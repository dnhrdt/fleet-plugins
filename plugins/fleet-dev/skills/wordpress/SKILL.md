---
name: wordpress
description: WordPress plugin development standards and patterns. Asset organisation, hook conventions, security practices. Use when developing WordPress plugins or themes.
version: 1.5.0
---

# WordPress Development Skill

---

## Asset Organisation (MANDATORY from v1.0.0)

**NO inline styles or scripts - EVER.**

**Structure:**
```
plugin-name/
├── assets/
│   ├── css/
│   │   ├── admin.css
│   │   └── frontend.css
│   └── js/
│       ├── admin.js
│       └── frontend.js
├── includes/
│   └── class-plugin-name.php
├── languages/
├── templates/
└── plugin-name.php
```

**Enqueue Pattern:**
```php
// In main plugin file or includes/class-*-admin.php
add_action('admin_enqueue_scripts', function($hook) {
    // Only on plugin pages
    if (strpos($hook, 'plugin-name') === false) return;

    wp_enqueue_style(
        'plugin-name-admin',
        plugin_dir_url(__FILE__) . 'assets/css/admin.css',
        [],
        '1.0.0'
    );

    wp_enqueue_script(
        'plugin-name-admin',
        plugin_dir_url(__FILE__) . 'assets/js/admin.js',
        ['jquery'],
        '1.0.0',
        true  // In footer
    );
});
```

**Why NO inline:**
- Cache-able by browser
- CSP (Content Security Policy) compatible
- Maintainable and testable
- Separates concerns

---

## Plugin Header (MANDATORY)

```php
<?php
/**
 * Plugin Name: Plugin Name
 * Plugin URI: https://example.com/plugin
 * Description: Brief description.
 * Version: 1.0.0
 * Requires at least: 6.0
 * Requires PHP: 7.4
 * Author: Author Name
 * Author URI: https://example.com
 * License: GPL v2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: plugin-name
 * Domain Path: /languages
 */

if (!defined('ABSPATH')) exit; // Security
```

---

## Security Basics

**Always:**
- Check `if (!defined('ABSPATH')) exit;` at top of every PHP file
- Use nonces for forms: `wp_nonce_field()`, `check_admin_referer()`
- Sanitize input: `sanitize_text_field()`, `absint()`, `esc_url()`
- Escape output: `esc_html()`, `esc_attr()`, `esc_url()`
- Check capabilities: `current_user_can('manage_options')`

**Form Example:**
```php
// In form
wp_nonce_field('plugin_action', 'plugin_nonce');

// On submit
if (!wp_verify_nonce($_POST['plugin_nonce'], 'plugin_action')) {
    wp_die('Security check failed');
}
```

---

## Future Sections (to be expanded)

- Hook naming conventions
- Database operations (wpdb)
- AJAX handling
- Settings API
- Custom Post Types
- WooCommerce integration patterns
- Multisite considerations
- Deployment specifics
- Translation/i18n

---

*This skill will grow with WordPress development experience.*
