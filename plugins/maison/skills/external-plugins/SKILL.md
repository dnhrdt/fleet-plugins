---
name: external-plugins
description: This skill should be used when the user asks about "Daniel's plugin", "Multilingual Multisite", "WPAllImport behavior", "ShortPixel", "SyncThing", "plugin conflicts", "translation tables", or needs to understand how external plugins interact with Maison code.
---

# External Plugins

## Purpose

Documentation of third-party plugins on Maison sites and their interaction patterns. Critical for avoiding conflicts.

## When to Use

- Debugging unexpected behavior
- Understanding hook conflicts
- Planning new features that touch media/products
- Isolating plugin interference

---

## Plugin Overview

| Plugin | Purpose | Conflict Risk |
|--------|---------|---------------|
| Daniel's Multilingual Multisite | Language sync | HIGH |
| WPAllImport | Product import | MEDIUM |
| ShortPixel | Image optimization | LOW |
| SyncThing | DE→US file sync | LOW |
| Force Regenerate Thumbnails | Thumbnail rebuild | LOW |

---

## Daniel's "WordPress Multilingual Multisite" Plugin

### Purpose

Language switching and content synchronization between Multisite sites.

### How It Works

**Hooks registered:**
- `add_attachment` - Syncs new attachments to other sites
- `edit_attachment` - Syncs metadata changes
- `delete_attachment` - Deletes ALL synced copies (cascade)

**Behavior:**
- Bidirectional sync (any site can be source)
- No filename check → Creates duplicates
- Cascade deletion → Deletes entire chain

### Translation Tables

| Table | Content |
|-------|---------|
| `{prefix}_posts_translations` | Post/Page/Product links |
| `{prefix}_terms_translations` | Term/Category links |

**Structure:**
```sql
-- Columns: id, type, data, 1, 3, 4, 6, 7, 8, 9, 10, 11 (Site IDs)
-- Link exists when both site columns have values
```

### Known Bug: Language Switcher on Shop Homepage

- **Problem:** Shows product URL instead of homepage URL
- **Cause:** `is_front_page()` checked before `is_shop()`
- **When:** Shop = Front Page, both conditions true
- **Status:** Bug report created for Daniel

**Key file:**
```
.../wordpress-multilingual-multisite/classes/class-wordpress-multilingual-multisite-public.php
```

### Conflicts with Our Code

| Conflict | Impact | Solution |
|----------|--------|----------|
| Bidirectional sync | We need unidirectional | Hook guard |
| Cascade deletion | Race condition | `remove_all_actions()` |
| No filename check | Duplicates | Three-step prevention |
| Meta interference | Corruption | Meta hook guards |

### Integration Pattern

```php
$removed = safe_remove_main_plugin_hooks();

try {
    wp_insert_attachment($data);
} finally {
    safe_restore_main_plugin_hooks($removed);
}
```

---

## WPAllImport

### Purpose

Nightly product import from CSV/XML files.

### Key Behavior

**Image Matching:**
- Searches `_wp_attached_file` by filename only
- Ignores path completely
- Takes lowest ID if multiple matches

**Implications:**
- Carryover products get wrong images
- Solution: Lookup-Table or Custom Field approach
- See `maison:wpallimport` skill for details

### Settings Location

- WP Admin → All Import → Manage Imports → Edit
- Function Editor: Bottom of import settings page

### functions.php Location

```
/wp-content/uploads/wpallimport/functions.php
```

Shared across all sites in Multisite.

---

## ShortPixel

### Purpose

Automatic image optimization (compression, WebP).

### Status on Maison

- Active on Site 1
- Auto-optimize enabled
- Processes new uploads automatically

### Implications

- No conflicts with our code
- Runs after upload complete
- Thumbnails optimized differently than originals

---

## SyncThing

### Purpose

File synchronization DE → US (one-way).

### How It Works

```
DE Multisite (Source)
    ↓ SyncThing
US Multisite (Target)
```

- Files sync automatically
- Thumbnails included
- One-way: DE → US only

### Implications

- US doesn't need thumbnail generation
- DE is source of truth for files
- US Bulk Register can reuse thumbnails

---

## Force Regenerate Thumbnails

### Purpose

Rebuild all thumbnail sizes for existing images after theme/plugin changes image dimensions.

### When to Use

- After changing registered image sizes in theme
- After adding new WooCommerce image dimensions
- When thumbnails appear blurry or wrong size

### Key Behavior

- Processes all attachments in media library
- Regenerates ALL registered sizes
- Can be run per-site in Multisite

### Implications

- Safe to use (no data loss)
- CPU intensive - run during low traffic
- SyncThing will propagate new thumbnails DE → US

---

## Plugin Interaction Matrix

| Action | Daniel's | WPAllImport | ShortPixel | Our Plugin |
|--------|----------|-------------|------------|------------|
| Upload on Site 1 | Syncs | - | Optimizes | Media Mirror |
| Product Import | - | Links images | - | - |
| Bulk Register | Would sync (guarded) | - | Optimizes | Creates |
| Cleanup | Would cascade (guarded) | - | - | DB-only |
| Resync | Would interfere (guarded) | - | - | Explicit |

---

## Debugging External Plugins

### Check Active Hooks

```php
global $wp_filter;
print_r($wp_filter['add_attachment']);
print_r($wp_filter['delete_attachment']);
```

### Check Daniel's Plugin Status

```php
class_exists('WordPress_Multilingual_Multisite_Sync');
class_exists('WordPress_Multilingual_Multisite_Media');
```

### Disable for Testing

```php
remove_all_actions('add_attachment');
remove_all_actions('edit_attachment');
remove_all_actions('delete_attachment');
```

### Isolate Plugin Interference

Same test WITHOUT Daniel's Plugin vs WITH:
- Session 99: 0% errors without, 42% with
- Proved race condition was external plugin

---

*Source: maison-media-manager Sessions 94-99, 158*
