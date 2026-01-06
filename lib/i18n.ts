import 'server-only';

export type Language = "en" | "ja" | "ko" | "zh-CN" | "zh-TW";

const loadDictionary = (lang: Language) => {
    switch (lang) {
        case "en": return import("@/locales/en/common.json").then(module => module.default);
        case "ja": return import("@/locales/ja/common.json").then(module => module.default);
        case "ko": return import("@/locales/ko/common.json").then(module => module.default);
        case "zh-CN": return import("@/locales/zh-CN/common.json").then(module => module.default);
        case "zh-TW": return import("@/locales/zh-TW/common.json").then(module => module.default);
        default: return import("@/locales/en/common.json").then(module => module.default);
    }
};

export const getDictionary = async (lang: Language) => {
    try {
        const dict = await loadDictionary(lang);
        return dict;
    } catch (error) {
        console.error(`Failed to load dictionary for ${lang}`, error);
        return await loadDictionary("en");
    }
};
