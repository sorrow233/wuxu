import 'server-only';

export type Language = "en" | "ja" | "ko" | "zh-CN" | "zh-TW";

const dictionaries = {
    en: () => import('@/locales/en.json').then((module) => module.default),
    ja: () => import('@/locales/ja.json').then((module) => module.default),
    ko: () => import('@/locales/ko.json').then((module) => module.default),
    "zh-CN": () => import('@/locales/zh-CN.json').then((module) => module.default),
    "zh-TW": () => import('@/locales/zh-TW.json').then((module) => module.default),
};

export const getDictionary = async (lang: Language) => {
    // If language is not supported, fallback to English
    if (dictionaries[lang]) {
        return dictionaries[lang]();
    }
    return dictionaries['en']();
};
