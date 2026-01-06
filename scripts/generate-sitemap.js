/* eslint-disable @typescript-eslint/no-require-imports */
const fs = require('fs');
const path = require('path');
const seoConfig = require('../seo-config.js');

const SITE_URL = seoConfig.siteUrl;
const ROUTES = Object.keys(seoConfig.routes);
const LANGUAGES = seoConfig.languages;

function generateSitemap() {
    const sitemapContent = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  ${ROUTES.map((route) => {
        // For each route, we generate an entry for each language
        return LANGUAGES.map((lang) => {
            // Construct URL: site.com/en or site.com/ja/about
            // For root route '/', it's site.com/en
            const langPath = lang === 'en' ? '' : `/${lang}`; // Keep 'en' at root or not? 
            // Actually based on my [lang] setup, 'en' is /en. 
            // Let's stick to the folder structure: /en, /ja, etc.
            // But usually default lang might be at root. 
            // Let's assume /en for explicit structure as per Next.js app/[lang]

            const url = `${SITE_URL}/${lang}${route === '/' ? '' : route}`;

            return `
  <url>
    <loc>${url}</loc>
    ${LANGUAGES.map(l => {
                const altUrl = `${SITE_URL}/${l}${route === '/' ? '' : route}`;
                return `<xhtml:link rel="alternate" hreflang="${l}" href="${altUrl}" />`;
            }).join('\n    ')}
  </url>`;
        }).join('');
    }).join('')}
</urlset>`;

    const publicDir = path.join(__dirname, '..', 'public');
    if (!fs.existsSync(publicDir)) {
        fs.mkdirSync(publicDir);
    }

    fs.writeFileSync(path.join(publicDir, 'sitemap.xml'), sitemapContent);
    console.log('✅ Sitemap generated at public/sitemap.xml');
}

generateSitemap();
