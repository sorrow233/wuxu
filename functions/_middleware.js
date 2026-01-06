import seoConfig from '../seo-config.js';

export async function onRequest(context) {
    const { request, next } = context;
    const url = new URL(request.url);
    const path = url.pathname;

    // Extract language from path e.g. /ja, /en
    // Assumes structure is /[lang]/... or just /[lang]
    const match = path.match(/^\/([a-zA-Z-]+)(\/|$)/);
    if (!match) {
        return next();
    }

    const lang = match[1];

    // Check if lang is supported in our config
    if (!seoConfig.languages.includes(lang)) {
        return next();
    }

    // Determine which route meta to use. 
    // For this simple portfolio, we mostly care about the home '/'
    // In a real app, map 'path' to 'seoConfig.routes' keys.
    // We'll normalize /ja to / and /ja/about to /about.

    // Logic: 
    // path = /ja -> route = /
    // path = /ja/foo -> route = /foo
    let route = path.replace(`/${lang}`, '') || '/';

    const meta = seoConfig.routes[route] && (seoConfig.routes[route][lang] || seoConfig.routes[route][seoConfig.defaultLanguage]);

    if (!meta) {
        return next();
    }

    // Fetch the original response (the static HTML)
    // Since we are using Next.js static export, the file at /ja/index.html ALREADY has logical metadata.
    // BUT the user workflow explicitly asked for "Edge Injection" to "change face" of index.html.
    // This might be redundant if Next.js does its job, but we follow the instruction for "Edge Injection".
    // This is useful if we were doing SPA with a single index.html. 
    // We will proceed to "Enhance" or "Ensure" the metadata is correct via Edge.

    const response = await next();

    if (!response.headers.get("content-type")?.includes("text/html")) {
        return response;
    }

    return new HTMLRewriter()
        .on("title", {
            element(element) {
                element.setInnerContent(meta.title);
            },
        })
        .on('meta[name="description"]', {
            element(element) {
                element.setAttribute("content", meta.description);
            },
        })
        .on('meta[property="og:title"]', {
            element(element) {
                element.setAttribute("content", meta.title);
            }
        })
        .on('meta[property="og:description"]', {
            element(element) {
                element.setAttribute("content", meta.description);
            }
        })
        .transform(response);
}
