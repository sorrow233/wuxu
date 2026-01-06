"use client"
/* eslint-disable @typescript-eslint/no-explicit-any */

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { ArrowRight, Github, Twitter } from "lucide-react"

export function Hero({ dict }: { dict: any }) {
    if (!dict) return null;

    return (
        <section className="relative flex min-h-[90vh] flex-col-reverse items-center justify-center overflow-hidden px-6 py-12 lg:flex-row lg:px-24">

            <div className="flex flex-1 flex-col justify-center gap-8 z-10 w-full max-w-3xl">
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.6, ease: "easeOut" }}
                    className="flex items-center gap-3"
                >
                    <span className="h-[1px] w-12 bg-zinc-400 dark:bg-zinc-600"></span>
                    <span className="text-sm font-medium tracking-widest uppercase text-zinc-500 dark:text-zinc-400">
                        {dict.location}
                    </span>
                </motion.div>

                <motion.h1
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
                    className="text-6xl font-bold tracking-tight sm:text-7xl lg:text-8xl text-zinc-900 dark:text-zinc-50 leading-[1.1]"
                >
                    {dict.titleStart}
                    <br />
                    <span className="text-zinc-400 dark:text-zinc-600">
                        {dict.titleEnd}
                    </span>
                    <span className="text-primary text-2xl lg:text-3xl ml-2 align-top">.</span>
                </motion.h1>

                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.4, ease: "easeOut" }}
                    className="max-w-xl text-lg text-zinc-600 dark:text-zinc-400 sm:text-xl leading-relaxed font-light"
                >
                    {dict.description}
                </motion.p>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.6, ease: "easeOut" }}
                    className="flex flex-wrap items-center gap-6 mt-4"
                >
                    <Button size="lg" className="rounded-full px-8 py-6 text-base shadow-none hover:shadow-lg transition-all duration-300 bg-zinc-900 text-white hover:bg-zinc-800 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200">
                        {dict.ctaProject}
                        <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                    <div className="flex gap-4">
                        <Button variant="ghost" size="icon" className="rounded-full hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                            <Github className="h-5 w-5 text-zinc-600 dark:text-zinc-400" />
                        </Button>
                        <Button variant="ghost" size="icon" className="rounded-full hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                            <Twitter className="h-5 w-5 text-zinc-600 dark:text-zinc-400" />
                        </Button>
                    </div>
                </motion.div>
            </div>

            <div className="relative flex-1 flex items-center justify-center lg:justify-end mb-16 lg:mb-0">
                <motion.div
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ duration: 1, delay: 0.2 }}
                    className="relative px-8"
                >
                    <div className="relative h-[400px] w-[300px] sm:h-[500px] sm:w-[400px] bg-zinc-100 dark:bg-zinc-900 overflow-hidden shadow-2xl skew-y-[-3deg] rounded-sm border border-zinc-200 dark:border-zinc-800">
                        {/* Placeholder for minimalist portrait or abstract art */}
                        <div className="absolute inset-0 flex items-center justify-center">
                            <span className="text-zinc-300 dark:text-zinc-700 font-mono tracking-widest text-xs rotate-[-3deg]">
                                [IMAGE / ARTWORK]
                            </span>
                        </div>
                    </div>
                    {/* Decorative element */}
                    <div className="absolute -z-10 bottom-[-20px] left-[-20px] h-full w-full border border-zinc-200 dark:border-zinc-800 skew-y-[-3deg] rounded-sm" />
                </motion.div>
            </div>
        </section>
    )
}
