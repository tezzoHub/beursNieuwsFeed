📈 beursNieuwsFeed
Automated scraper for collecting financial news items from
https://www.beurs.nl/nieuws.

The scraper runs on GitHub Actions and publishes its output as a JSON feed via GitHub Pages.
This feed can be consumed by WordPress or any other system that supports JSON.

---

📡 Live JSON Feed
The latest news feed is publicly available via GitHub Pages:
https://tezzohub.github.io/beursNieuwsFeed/data/nieuws.json
This endpoint is updated automatically every x minutes and can be used directly inside WordPress or external applications.

---

📁 Repository structuur

beursNieuwsFeed/
│
├── src/
│   └── scraper.py
│
├── data/
│   └── nieuws.json        (wordt automatisch gevuld)
│
├── .github/
│   └── workflows/
│       └── scrapeBeursNieuwsWorkflow.yml
│
├── README.md
└── requirements.txt

---

🚀 Automation (GitHub Actions)
The scraper is executed automatically through the workflow
scrapeBeursNieuwsWorkflow.yml, which:

* visits the target website
* extracts the latest news items
* updates data/nieuws.json
* commits changes back to the repository
* publishes the JSON feed via GitHub Pages  

---

🔄 Workflow Schedule
The scraper runs:
* every x minutes via cron
* on demand via “Run workflow” in GitHub Actions

Workflow steps:
* Install Python
* Install dependencies
* Execute scraper.py
* Commit & push updated JSON to main
* Publish the feed through GitHub Pages  

---

📦 JSON Schema
Each news item in nieuws.json follows this structure:

{
  "id": "string",               // Unique hash based on title + link
  "categorie": "string",        // Category of the news item
  "titel": "string",            // Article title
  "link": "string",             // Absolute URL to the article
  "intro": "string",            // Short introduction text
  "published_at": "string",     // Publication timestamp (ISO)
  "scraped_at": "string"        // Timestamp of the scraper run (ISO)
}

---

🌐 Using the JSON Feed in WordPress
This project includes a lightweight WordPress integration that consumes the JSON feed and renders it using native WordPress RSS‑block
styling. The integration is implemented as a shortcode that can be placed inside any post, page, or theme block.

// Fetching the JSON feed (add the following to your theme's functions.php)
function beursnieuws_get_data() {
    $cache_key = 'beursnieuws_cache';
    $cached = get_transient($cache_key);

// Return cached data if available
    if ($cached !== false) {
        return $cached;
    }

  $url = 'https://tezzohub.github.io/beursNieuwsFeed/data/nieuws.json';
  $response = wp_remote_get($url, ['timeout' => 10]);
    
  // Handle request errors
    if (is_wp_error($response)) {
        return [];
    }

  $body = wp_remote_retrieve_body($response);
  $data = json_decode($body, true);

  // Validate JSON structure
    if (!is_array($data)) {
        return [];
    }

  // Cache for 5 minutes
    set_transient($cache_key, $data, 5 * MINUTE_IN_SECONDS);

  return $data;
}

// SHORTCODE:
function beursnieuws_shortcode($atts) {
    $atts = shortcode_atts([
      'limit' => 20,
      'view'  => 'full' // options full,telex
], $atts);

$items = beursnieuws_get_data();
$items = array_slice($items, 0, intval($atts['limit']));

if (empty($items)) {
    return '<p>Geen nieuws beschikbaar.</p>';
}

ob_start();

  
// TELEX VIEW (Only titles, WP-rss CSS style)
if ($atts['view'] === 'telex') {

echo '<ul class="wp-block-rss">';

foreach ($items as $item) {
          echo '<li class="wp-block-rss__item">';
          echo '<a class="wp-block-rss__item-title" href="' . esc_url($item['link']) . '" target="_blank" rel="noopener">';
            echo esc_html($item['titel']);
            echo '</a>';
            echo '</li>';
        }

echo '</ul>';

return ob_get_clean();
}

// FULL VIEW (Standard)
echo '<div class="beursnieuws-list">';

foreach ($items as $item) {
    ?>
    <article class="beursnieuws-item">
       <h3 class="beursnieuws-title">
         <a href="<?php echo esc_url($item['link']); ?>" target="_blank" rel="noopener">
             <?php echo esc_html($item['titel']); ?>
         </a>
       </h3>

<p class="beursnieuws-meta">
    <?php echo esc_html($item['categorie']); ?> —
    <?php echo esc_html($item['published_at']); ?>
</p>

<?php if (!empty($item['intro'])): ?>
<p class="beursnieuws-intro">
                  <?php echo esc_html($item['intro']); ?>
</p>
        <?php endif; ?>
        </article>
        <?php
    }

echo '</div>';

return ob_get_clean();
}
add_shortcode('beursnieuws', 'beursnieuws_shortcode');

---

📝 Toekomstige uitbreidingen

- In shortcode replace IF to Switch
- Source toevoegen aan item (to be discussed)
