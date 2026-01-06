import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { match } from "@formatjs/intl-localematcher";
import Negotiator from "negotiator";

const locales = ["en", "ja", "ko", "zh-CN", "zh-TW"];
const defaultLocale = "en";

function getLocale(request: NextRequest): string {
    // 1. Check cookie for manual preference
    const cookieLocale = request.cookies.get("NEXT_LOCALE")?.value;
    if (cookieLocale && locales.includes(cookieLocale)) {
        return cookieLocale;
    }

    // 2. Check Accept-Language header
    const headers = { "accept-language": request.headers.get("accept-language") || "" };
    const languages = new Negotiator({ headers }).languages();

    try {
        // 3. Match against supported locales
        return match(languages, locales, defaultLocale);
    } catch (e) {
        return defaultLocale;
    }
}

export function middleware(request: NextRequest) {
    const { pathname } = request.nextUrl;

    // Check if there is any supported locale in the pathname
    const pathnameHasLocale = locales.some(
        (locale) => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
    );

    if (pathnameHasLocale) return;

    // Redirect if no locale found in path
    const locale = getLocale(request);

    // Construct new URL
    const newUrl = new URL(`/${locale}${pathname === '/' ? '' : pathname}`, request.url);
    newUrl.search = request.nextUrl.search;

    return NextResponse.redirect(newUrl);
}

export const config = {
    matcher: [
        // Skip all internal paths (_next, assets, api)
        '/((?!_next|favicon.ico|api|.*\\..*).*)',
    ],
};
