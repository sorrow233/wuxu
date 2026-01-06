import 'server-only';

export type Language = "en" | "ja" | "ko" | "zh-CN" | "zh-TW";

const dictionaries = {
    en: () => import("@/locales/en/common.json").then((module) => module.default),
    ja: () => import("@/locales/ja/common.json").then((module) => module.default),
    ko: () => import("@/locales/ko/common.json").then((module) => module.default),
    "zh-CN": () => import("@/locales/zh-CN/common.json").then((module) => module.default),
    "zh-TW": () => import("@/locales/zh-TW/common.json").then((module) => module.default),
};

export const getDictionary = async (lang: Language) => {
    return dictionaries[lang]?.() ?? dictionaries.en();
};
