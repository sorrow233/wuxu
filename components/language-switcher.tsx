"use client"

import * as React from "react"
import { usePathname, useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Languages } from "lucide-react"

const languages = [
    { code: "en", label: "English" },
    { code: "ja", label: "日本語" },
    { code: "ko", label: "한국어" },
    { code: "zh-CN", label: "简体中文" },
    { code: "zh-TW", label: "繁體中文" },
]

export function LanguageSwitcher() {
    const pathname = usePathname()
    const router = useRouter()
    const [isOpen, setIsOpen] = React.useState(false)

    // Determine current language from path
    const currentLang = pathname?.split("/")[1] || "en"

    const handleSwitch = (langCode: string) => {
        if (!pathname) return
        const segments = pathname.split("/")
        segments[1] = langCode
        const newPath = segments.join("/")
        router.push(newPath)
        setIsOpen(false)
    }

    return (
        <div className="fixed bottom-6 right-6 z-50">
            {isOpen && (
                <div className="mb-2 flex flex-col gap-1 rounded-lg border bg-background p-2 shadow-lg animate-in slide-in-from-bottom-2 fade-in">
                    {languages.map((lang) => (
                        <Button
                            key={lang.code}
                            variant={currentLang === lang.code ? "secondary" : "ghost"}
                            size="sm"
                            className="justify-start whitespace-nowrap"
                            onClick={() => handleSwitch(lang.code)}
                        >
                            {lang.label}
                        </Button>
                    ))}
                </div>
            )}
            <Button
                variant="outline"
                size="icon"
                className="h-12 w-12 rounded-full shadow-md bg-background"
                onClick={() => setIsOpen(!isOpen)}
                aria-label="Switch Language"
            >
                <Languages className="h-6 w-6" />
            </Button>
        </div>
    )
}
