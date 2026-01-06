import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { match } from '@formatjs/intl-localematcher'
import Negotiator from 'negotiator'

const locales = ['en', 'ja', 'ko', 'zh-CN', 'zh-TW']
const defaultLocale = 'en' // Priority 3: English

function getLocale(request: NextRequest): string {
    // Priority 1: Manual (Cookie)
    const cookieLocale = request.cookies.get('NEXT_LOCALE')?.value
    if (cookieLocale && locales.includes(cookieLocale)) {
        return cookieLocale
    }

    // Priority 2: System (Header)
    const headers = { 'accept-language': request.headers.get('accept-language') || '' }
    const languages = new Negotiator({ headers }).languages()

    try {
        return match(languages, locales, defaultLocale)
    } catch (e) {
        return defaultLocale
    }
}

export function middleware(request: NextRequest) {
    const { pathname } = request.nextUrl

    // Skip files and API
    if (
        pathname.startsWith('/_next') ||
        pathname.startsWith('/api') ||
        pathname.startsWith('/favicon.ico') ||
        pathname.match(/\.(png|jpg|jpeg|svg|css|js|map|json|ico)$/)
    ) {
        return
    }

    // Check if pathname has locale
    const pathnameHasLocale = locales.some(
        (locale) => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
    )

    if (pathnameHasLocale) {
        return
    }

    // Redirect if missing locale
    const locale = getLocale(request)
    request.nextUrl.pathname = `/${locale}${pathname}`
    return NextResponse.redirect(request.nextUrl)
}

export const config = {
    matcher: [
        // Skip all internal paths (_next)
        '/((?!_next|favicon.ico|api).*)',
    ],
}
