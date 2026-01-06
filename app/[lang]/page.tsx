import { Hero } from "@/components/sections/hero";
import { Projects } from "@/components/sections/projects";
import { About } from "@/components/sections/about";
import { Contact } from "@/components/sections/contact";
import { getDictionary, Language } from "@/lib/i18n";
import { Metadata } from "next";

// Import seo-config
// Import seo-config
// eslint-disable-next-line @typescript-eslint/no-require-imports
const seoConfig = require("@/seo-config");

type Props = {
    params: Promise<{ lang: Language }>;
};

export async function generateStaticParams() {
    return seoConfig.languages.map((lang: string) => ({
        lang: lang,
    }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
    const { lang } = await params;
    const routeConfig = seoConfig.routes["/"];
    const meta = routeConfig[lang] || routeConfig[seoConfig.defaultLanguage];

    return {
        title: meta.title,
        description: meta.description,
        alternates: {
            canonical: `${seoConfig.siteUrl}/${lang === 'en' ? '' : lang}`,
            languages: {
                'en': `${seoConfig.siteUrl}/en`,
                'ja': `${seoConfig.siteUrl}/ja`,
                'ko': `${seoConfig.siteUrl}/ko`,
                'zh-CN': `${seoConfig.siteUrl}/zh-CN`,
                'zh-TW': `${seoConfig.siteUrl}/zh-TW`,
            }
        }
    };
}

export default async function Home({ params }: Props) {
    const { lang } = await params;
    const dict = await getDictionary(lang);

    return (
        <main className="flex min-h-screen flex-col items-center justify-between overflow-x-hidden bg-background text-foreground">
            <Hero dict={dict.hero} />
            <Projects dict={dict.projects} common={dict.common} />
            <About dict={dict.about} common={dict.common} />
            <Contact dict={dict.contact} common={dict.common} />
        </main>
    );
}
