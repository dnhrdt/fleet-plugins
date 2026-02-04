---
name: wordpress-patterns
description: This skill should be used when the user asks about "multisite patterns", "hook management", "switch_to_blog", "site_option vs option", "wp_delete_attachment", "batch processing", "duplicate prevention", or encounters WordPress Multisite data corruption issues. Provides 8 critical patterns learned from 176 sessions.
---

# WordPress Multisite Patterns

## Purpose

Critical patterns for WordPress Multisite development that prevent data corruption. Each pattern was learned through production incidents on Maison sites (maisoncommon.com).

## When to Use

- Developing Multisite plugins/themes
- Debugging cross-site synchronization issues
- Working with attachments across sites
- Optimizing bulk operations

---

## Pattern Overview

| # | Pattern | Prevents |
|---|---------|----------|
| 1 | Hook Guard | Infinite loops, race conditions |
| 2 | try-finally for switch_to_blog | Context corruption |
| 3 | site_option vs option | Silent setting failures |
| 4 | DB-Only Deletion | Unintended file deletion |
| 5 | Three-Step Duplicate Prevention | Duplicate attachments |
| 6 | Context Flag | Cross-system interference |
| 7 | Batch Processing | Timeouts, memory exhaustion |
| 8 | SQL Batch Loading | N+1 query performance |

---

## Pattern 1: Hook Guard (CRITICAL)

**Problem:** External plugins (Daniel's Multilingual Multisite) hook into WordPress events causing infinite loops and race conditions.

**Solution:**

```php
try {
    $removed = safe_remove_main_plugin_hooks();

    // Perform operation
    wp_insert_attachment($data);

} finally {
    safe_restore_main_plugin_hooks($removed);
}
```

**Hooks to guard:**

| Hook | Risk | Guard Before |
|------|------|--------------|
| `add_attachment` | Bidirectional sync loop | `wp_insert_attachment()` |
| `edit_attachment` | Metadata corruption | Metadata updates |
| `delete_attachment` | Cascade deletion | Cleanup operations |
| `updated_post_meta` | Meta sync interference | `update_post_meta()` |
| `added_post_meta` | Meta sync interference | `add_post_meta()` |
| `deleted_post_meta` | Meta sync interference | `delete_post_meta()` |

---

## Pattern 2: try-finally for switch_to_blog

**Problem:** Unrestore context corrupts WordPress state.

**Solution:**

```php
try {
    switch_to_blog($site_id);
    $result = $wpdb->get_results($query);
} finally {
    restore_current_blog();  // ALWAYS restore
}
```

**Consequences if not restored:**
- Wrong site tables accessed
- Wrong options returned
- Uploads go to wrong directory

---

## Pattern 3: site_option vs option (CRITICAL)

**Problem:** Using wrong API = silent failure (90+ min debug time).

```php
// WRONG - Site-specific:
update_option('my_setting', $value);
get_option('my_setting', $default);

// CORRECT - Network-wide:
update_site_option('my_setting', $value);
get_site_option('my_setting', $default);
```

**Rule:** ALWAYS use `get_site_option()` / `update_site_option()` for plugin settings in Multisite.

---

## Pattern 4: DB-Only Deletion

**Problem:** `wp_delete_attachment($id, true)` deletes files too.

**Solution:**

```php
add_filter('wp_delete_file', '__return_false');
wp_delete_attachment($id, true);
remove_filter('wp_delete_file', '__return_false');
```

---

## Pattern 5: Three-Step Duplicate Prevention

```php
// Step 1: Already synced?
$existing = get_post_id_from_meta('_mls_synced_id', $site_1_id);
if ($existing) return;

// Step 2: Exists by filename?
$by_filename = get_attachments_by_filename($filename);
if ($by_filename) {
    update_post_meta($by_filename, '_mls_synced_id', $site_1_id);
    return;
}

// Step 3: Create new
wp_insert_attachment($data);
```

---

## Pattern 6: Context Flag

**Problem:** Multiple systems trigger on same events.

```php
global $mmm_bulk_register_running;
$mmm_bulk_register_running = true;

try {
    // Operations
} finally {
    $mmm_bulk_register_running = false;
}

// In other handler:
if (!empty($mmm_bulk_register_running)) return;
```

---

## Pattern 7: Batch Processing

```php
$start_time = time();
$timeout = 240;  // 4 min buffer

foreach ($items as $item) {
    if ((time() - $start_time) >= $timeout) break;
    process_item($item);
}
```

**Tested batch sizes:**

| Operation | Batch Size |
|-----------|------------|
| Filesystem Scan | 1000 |
| Cleanup | 500 |
| Bulk Register | 50 |
| Resync | 100 |

---

## Pattern 8: SQL Batch Loading

**Problem:** N+1 queries (45x slower).

```php
// Load ALL at once
$site_1_ids = $wpdb->get_col("SELECT ID FROM wp_posts WHERE post_type = 'attachment'");
$synced_ids = $wpdb->get_col("SELECT meta_value FROM wp_6_postmeta WHERE meta_key = '_mls_synced_id'");

// Compare in PHP
$missing = array_diff($site_1_ids, $synced_ids);
```

**Performance:** 37 min → 30 sec (45x faster)

---

## Multisite Structure Reference

### DE Multisite (maisoncommon.com) - Prefix: wpzu_

| Site ID | URL | Purpose |
|---------|-----|---------|
| 1 | maisoncommon.com | Main site |
| 6 | maisoncommon.com/en | EN Website |
| 7 | shop.maisoncommon.com/en | EN Shop |
| 8 | b2b.maisoncommon.com | B2B Shop |
| 9 | pos.maisoncommon.com | POS System |
| 10 | shop.maisoncommon.com/de | DE Shop |
| 11 | order.maisoncommon.com | Order Portal |

### Key Meta Keys

| Meta Key | Purpose |
|----------|---------|
| `_wp_attached_file` | Relative path to file |
| `_wp_attachment_metadata` | Dimensions, thumbnails |
| `_mls_synced_id` | Site 1 parent ID (child sites only) |

---

*Source: maison-media-manager Sessions 1-176*
