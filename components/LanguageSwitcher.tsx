"use client"

import { usePathname, useRouter } from "next/navigation"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Globe } from "lucide-react"

const languages = [
    { code: "en", label: "English" },
    { code: "ja", label: "日本語" },
    { code: "ko", label: "한국어" },
    { code: "zh-CN", label: "简体中文" },
    { code: "zh-TW", label: "繁體中文" },
]

export function LanguageSwitcher({ currentLang }: { currentLang: string }) {
    const router = useRouter()
    const pathname = usePathname()
    const [isOpen, setIsOpen] = useState(false)

    const handleLanguageChange = (newLang: string) => {
        // 1. Set Cookie for Middleware
        document.cookie = `NEXT_LOCALE=${newLang}; path=/; max-age=31536000`

        // 2. Set LocalStorage for Client Priority checks
        localStorage.setItem("user-preference", newLang)

        // 3. Redirect
        // Ensure we replace the first segment if it matches current lang
        // pathname is like /en or /en/about
        const segments = pathname.split('/')
        if (segments[1] === currentLang) {
            segments[1] = newLang
            const newPath = segments.join('/')
            router.push(newPath)
        } else {
            // Fallback if something weird, simple replace
            const newPath = pathname.replace(`/${currentLang}`, `/${newLang}`)
            router.push(newPath)
        }
        setIsOpen(false)
    }

    return (
        <div className="fixed top-4 right-4 z-50">
            <div className="relative">
                <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setIsOpen(!isOpen)}
                    className="rounded-full bg-background/50 backdrop-blur-sm border shadow-sm hover:bg-accent"
                >
                    <Globe className="h-5 w-5" />
                </Button>
                {isOpen && (
                    <div className="absolute right-0 mt-2 w-40 rounded-md bg-background border shadow-lg ring-1 ring-black ring-opacity-5 overflow-hidden">
                        <div className="py-1">
                            {languages.map((lang) => (
                                <button
                                    key={lang.code}
                                    onClick={() => handleLanguageChange(lang.code)}
                                    className={`block w-full text-left px-4 py-2 text-sm transition-colors ${currentLang === lang.code
                                            ? "bg-accent text-accent-foreground font-medium"
                                            : "text-muted-foreground hover:bg-accent/50 hover:text-accent-foreground"
                                        }`}
                                >
                                    {lang.label}
                                </button>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
