export type Language = "en" | "ja" | "ko" | "zh-CN" | "zh-TW";

export const dictionaries = {
    en: {
        hero: {
            location: "Tokyo, Japan 🇯🇵",
            titleStart: "Dev &",
            titleEnd: "Lifestyler.",
            description: "Full-Stack Developer based in Tokyo. Crafting digital experiences with a touch of minimalism and efficiency.",
            ctaProject: "Check Projects",
        },
        projects: {
            title: "Featured Projects",
            description: "A selection of things I've built."
        },
        about: {
            title: "About Me",
            description1: "Hello! I'm a software developer originally from [Your Country], now living in",
            description2: "Tokyo, Japan",
            description3: "I arrived in October 2024 and I'm currently studying Japanese at Kyoritsu Japanese Language Academy while continuing my journey as a Full-Stack Developer.",
            description4: "My goal is to blend technical excellence with the aesthetic sensibility I admire in Japanese design. When I'm not coding, I'm exploring the backstreets of Bunkyo-ku or trying to cook with my limited kitchen gear.",
            techStack: "Tech Stack"
        },
        contact: {
            title: "Let's Create Something Together",
            description: "Whether you have a question, a project idea, or just want to say hi in Tokyo, my inbox is always open.",
            cta: "Say Hello"
        }
    },
    ja: {
        hero: {
            location: "東京、日本 🇯🇵",
            titleStart: "開発者 &",
            titleEnd: "ライフスタイラー",
            description: "東京を拠点とするフルスタック開発者。ミニマリズムと効率性を融合させたデジタル体験を作り出します。",
            ctaProject: "プロジェクトを見る",
        },
        projects: {
            title: "主要プロジェクト",
            description: "これまでに開発した主な作品。"
        },
        about: {
            title: "私について",
            description1: "こんにちは！ソフトウェア開発者です。現在は",
            description2: "日本の東京",
            description3: "に住んでいます。2024年10月に来日し、共立日語学院で日本語を学びながら、フルスタック開発者としての活動を続けています。",
            description4: "私の目標は、技術的な卓越性と、私が敬愛する日本デザインの美的感覚を融合させることです。コーディングをしていない時は、文京区の裏道を散策したり、限られた調理器具で料理に挑戦したりしています。",
            techStack: "技術スタック"
        },
        contact: {
            title: "一緒に何か作りませんか",
            description: "質問、プロジェクトのアイデア、あるいは東京での挨拶など、いつでもご連絡ください。",
            cta: "こんにちはと言う"
        }
    },
    // Placeholders for other languages (falling back to English structure for simplicity in this demo, but keys are here)
    ko: {
        hero: { location: "도쿄, 일본 🇯🇵", titleStart: "Dev &", titleEnd: "Lifestyler.", description: "도쿄 기반 풀스택 개발자.", ctaProject: "프로젝트 확인" },
        projects: { title: "주요 프로젝트", description: "제가 만든 것들입니다." },
        about: { title: "소개", description1: "안녕하세요!", description2: "도쿄", description3: "2024년 10월 도착.", description4: "기술과 미학의 조화.", techStack: "기술 스택" },
        contact: { title: "함께 만들어요", description: "언제든 연락주세요.", cta: "인사하기" }
    },
    "zh-CN": {
        hero: { location: "日本东京 🇯🇵", titleStart: "开发 &", titleEnd: "生活家", description: "由于东京的全栈开发者。", ctaProject: "查看项目" },
        projects: { title: "精选项目", description: "我的一些作品。" },
        about: { title: "关于我", description1: "你好！", description2: "东京", description3: "2024年10月抵达。", description4: "追求技术与美学的融合。", techStack: "技术栈" },
        contact: { title: "联系我", description: "欢迎随时联系。", cta: "打个招呼" }
    },
    "zh-TW": {
        hero: { location: "日本東京 🇯🇵", titleStart: "開發 &", titleEnd: "生活家", description: "居於東京的全端開發者。", ctaProject: "查看專案" },
        projects: { title: "精選專案", description: "我的一些作品。" },
        about: { title: "關於我", description1: "你好！", description2: "東京", description3: "2024年10月抵達。", description4: "追求技術與美學的融合。", techStack: "技術棧" },
        contact: { title: "聯絡我", description: "歡迎隨時聯絡。", cta: "打個招呼" }
    }
};

export const getDictionary = (lang: Language) => {
    return dictionaries[lang] || dictionaries['en'];
};
