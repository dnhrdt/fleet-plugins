---
name: wpallimport
description: This skill should be used when the user asks about "WPAllImport", "product import", "image matching", "carryover problem", "site1_id_to_local_id", "ids_to_images", "lookup table", "functions.php", or needs to configure nightly imports on Maison sites.
---

# WPAllImport Guide

## Purpose

Configuration and troubleshooting for WPAllImport product imports on Maison sites. Covers the Carryover Problem and its solutions.

## When to Use

- Setting up product imports
- Debugging image assignment issues
- Configuring functions.php helpers
- Understanding import chains

---

## The Carryover Problem

### How WPAllImport Image Matching Works

WPAllImport's "Use images currently in Media Library" option:
- Searches ONLY by **filename** (basename)
- **Ignores paths** completely
- Takes **lowest ID** if multiple matches

### Why This Breaks

Carryover products (same article in new collection) have identical filenames:

```
Collection 232: lse-import/bilder/232/9400700_420/9400700_420_1.jpg
Collection 264: lse-import/bilder/264/9400700_420/9400700_420_1.jpg
```

WPAllImport finds both, takes lowest ID (old collection) → **Wrong image!**

---

## Solution 1: Lookup-Table System (Recommended)

### Architecture

Assign images **during** product import, not via Images Section.

```
Product Import Start
    ↓
Build Lookup Table (1 query, ~600ms)
    ↓
Per Product: SKU → Lookup → Assign Images
    ↓
Product Import End
```

### functions.php Location

```
/wp-content/uploads/wpallimport/functions.php
```

Both DE and US Multisites need this file.

### Implementation

```php
// Hook: Before import starts
add_action('pmxi_before_xml_import', 'mmm_build_image_lookup');

// Hook: Per product saved
add_action('pmxi_saved_post', 'mmm_assign_images_from_lookup', 10, 3);
```

**Build Lookup Table:**

```php
function mmm_build_image_lookup($import_id) {
    global $wpdb, $mmm_image_lookup;

    $results = $wpdb->get_results("
        SELECT post_id, meta_value as file_path
        FROM {$wpdb->postmeta}
        WHERE meta_key = '_wp_attached_file'
        AND meta_value LIKE 'lse-import/bilder/%'
    ");

    $mmm_image_lookup = [];
    foreach ($results as $row) {
        if (preg_match('#lse-import/bilder/(\d+)/(\d+_\d+)/#', $row->file_path, $m)) {
            $key = $m[1] . '/' . $m[2];  // "264/9400700_420"
            $mmm_image_lookup[$key][] = $row->post_id;
        }
    }
}
```

**Assign Images:**

```php
function mmm_assign_images_from_lookup($post_id, $xml_node, $import_id) {
    global $mmm_image_lookup;

    $sku = get_post_meta($post_id, '_sku', true);
    $parts = explode('-', $sku);

    $kollektion = $parts[1];
    $produktnummer = $parts[2];
    $prefix = $kollektion . '/' . $produktnummer . '_';

    foreach ($mmm_image_lookup as $key => $attachment_ids) {
        if (strpos($key, $prefix) === 0) {
            sort($attachment_ids);
            set_post_thumbnail($post_id, $attachment_ids[0]);

            if (count($attachment_ids) > 1) {
                $gallery = array_slice($attachment_ids, 1);
                update_post_meta($post_id, '_product_image_gallery', implode(',', $gallery));
            }
            return;
        }
    }

    // No image → Draft (B2C only)
    if (in_array(get_current_blog_id(), [7, 10])) {
        wp_update_post(['ID' => $post_id, 'post_status' => 'draft']);
    }
}
```

---

## Solution 2: Custom Field Approach

For CSV imports with Attachment IDs:

### WPAllImport Configuration

1. **Images Section:** Leave **EMPTY**
2. **Custom Fields:** `_thumbnail_id` = `[site1_id_to_local_id({images[1]})]`

### Function

```php
function site1_id_to_local_id($site1_id) {
    if (empty($site1_id)) return '';

    $site1_id = trim(explode(',', $site1_id)[0]);
    if (!is_numeric($site1_id)) return '';

    if (get_current_blog_id() == 1) {
        return (int)$site1_id;
    }

    global $wpdb;
    $local_id = $wpdb->get_var($wpdb->prepare(
        "SELECT post_id FROM {$wpdb->postmeta}
         WHERE meta_key = '_mls_synced_id' AND meta_value = %s",
        $site1_id
    ));

    return $local_id ? (int)$local_id : '';
}
```

---

## Legacy: ids_to_images()

For imports needing paths instead of IDs:

```php
function ids_to_images($ids_string) {
    if (empty($ids_string)) return '';

    $ids = explode(',', $ids_string);
    $paths = [];
    $upload_dir = wp_upload_dir();

    global $wpdb;

    foreach ($ids as $site1_id) {
        $site1_id = trim($site1_id);
        if (!is_numeric($site1_id)) continue;

        $local_id = $wpdb->get_var($wpdb->prepare(
            "SELECT post_id FROM {$wpdb->postmeta}
             WHERE meta_key = '_mls_synced_id' AND meta_value = %s",
            $site1_id
        ));

        if ($local_id) {
            $file = get_attached_file($local_id);
            if ($file) {
                $paths[] = str_replace($upload_dir['basedir'] . '/', '', $file);
            }
        }
    }

    return implode(',', $paths);
}
```

**Limitation:** Does NOT solve Carryover problem (WPAllImport still extracts basename).

---

## Critical Settings

| Setting | Correct Value | Problem if Wrong |
|---------|---------------|------------------|
| `is_update_images` | 0 | Overwrites assignments |
| `is_update_attachments` | **0** | Deletes gallery links! |
| `is_keep_attachments` | 1 | Loses existing |

**Fix via SQL:**

```sql
UPDATE {prefix}_pmxi_imports
SET options = REPLACE(options,
    '"is_update_attachments";s:1:"1"',
    '"is_update_attachments";s:1:"0"')
WHERE options LIKE '%"is_update_attachments";s:1:"1"%';
```

---

## Import Chain (Daisy-Chain)

### DE Chain

```
Site 10 (shop/de) → Site 9 (pos) → Site 8 (b2b) → Site 7 (shop/en) → Site 11 (order)
```

### Trigger URL Format

```
https://{domain}/?wpai_cron_run_key={key}&id={import_id}&processing=1
```

---

## File Paths

### Product Images

```
/wp-content/uploads/lse-import/bilder/{collection}/{product_color}/
```

Example: `lse-import/bilder/264/9400700_420/9400700_420_1.jpg`

### Category Images

```
/wp-content/uploads/lse-import/categories/{CategoryName}_{1|2}.jpg
```

---

## Debugging

### Check Import Log

```bash
ls -la /wp-content/uploads/wpallimport/logs/
```

### Manual Trigger

```bash
curl "https://domain.com/?wpai_cron_run_key=KEY&id=ID&processing=1"
```

### Verify Lookup Table

```sql
SELECT COUNT(*) as images,
       SUBSTRING_INDEX(meta_value, '/', 3) as collection
FROM wp_postmeta
WHERE meta_key = '_wp_attached_file'
  AND meta_value LIKE 'lse-import/bilder/%'
GROUP BY collection;
```

---

*Source: maison-media-manager Sessions 164-176*
