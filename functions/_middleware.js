import seoConfig from '../seo-config.js';

export async function onRequest(context) {
    const { request, next } = context;
    const url = new URL(request.url);
    const path = url.pathname;

    // 1. Auto-Detection for Root Path '/'
    if (path === '/') {
        const acceptLanguage = request.headers.get('Accept-Language');
        let targetLang = seoConfig.defaultLanguage; // Default to 'en'

        if (acceptLanguage) {
            // Basic parsing of Accept-Language header (e.g., "ja,en-US;q=0.9,en;q=0.8")
            const preferredLangs = acceptLanguage.split(',').map(lang => lang.split(';')[0].trim());

            for (const pref of preferredLangs) {
                // Check exact match (e.g., zh-CN)
                if (seoConfig.languages.includes(pref)) {
                    targetLang = pref;
                    break;
                }
                // Check primary subtag (e.g., zh in zh-CN, or ja in ja-JP)
                const base = pref.split('-')[0];
                const match = seoConfig.languages.find(l => l.startsWith(base));
                if (match) {
                    targetLang = match;
                    break;
                }
            }
        }

        // Redirect to the detected language
        return Response.redirect(`${url.origin}/${targetLang}`, 302);
    }

    // 2. Multilingual SEO Injection for /[lang]/* paths
    const match = path.match(/^\/([a-zA-Z-]+)(\/|$)/);
    if (!match) {
        return next();
    }

    const lang = match[1];

    if (!seoConfig.languages.includes(lang)) {
        return next();
    }

    let route = path.replace(`/${lang}`, '') || '/';
    const meta = seoConfig.routes[route] && (seoConfig.routes[route][lang] || seoConfig.routes[route][seoConfig.defaultLanguage]);

    if (!meta) {
        return next();
    }

    const response = await next();

    if (!response.headers.get("content-type")?.includes("text/html")) {
        return response;
    }

    return new HTMLRewriter()
        .on("title", { element(e) { e.setInnerContent(meta.title); } })
        .on('meta[name="description"]', { element(e) { e.setAttribute("content", meta.description); } })
        .on('meta[property="og:title"]', { element(e) { e.setAttribute("content", meta.title); } })
        .on('meta[property="og:description"]', { element(e) { e.setAttribute("content", meta.description); } })
        .transform(response);
}
