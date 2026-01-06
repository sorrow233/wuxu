module.exports = {
    // Domain config
    siteUrl: "https://wuxu.catzz.work",
    defaultLanguage: "en",
    languages: ["en", "ja", "ko", "zh-CN", "zh-TW"],

    // Route-specific metadata
    routes: {
        "/": {
            en: {
                title: "Tokyo Lifestyler | Full-Stack Developer",
                description: "Personal website of a Tokyo-based software developer. Exploring code, life, and minimalism.",
            },
            ja: {
                title: "Tokyo Lifestyler | フルスタックエンジニア",
                description: "東京在住のソフトウェア開発者。コードと生活、そしてミニマリズムを探求する個人サイト。",
            },
            ko: {
                title: "Tokyo Lifestyler | 풀스택 개발자",
                description: "도쿄에 거주하는 소프트웨어 개발자. 코드, 생활, 미니멀리즘을 탐구하는 개인 웹사이트.",
            },
            "zh-CN": {
                title: "Tokyo Lifestyler | 全栈开发者",
                description: "居于东京的软件开发者。探索代码、生活与极简主义的个人网站。",
            },
            "zh-TW": {
                title: "Tokyo Lifestyler | 全端開發者",
                description: "居於東京的軟體開發者。探索程式碼、生活與極簡主義的個人網站。",
            },
        },
        // Future routes can be added here
    },
};
