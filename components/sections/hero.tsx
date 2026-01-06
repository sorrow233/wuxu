"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { ArrowRight, Github, Twitter } from "lucide-react"

export function Hero() {
    return (
        <section className="relative flex min-h-[90vh] flex-col-reverse items-center justify-center overflow-hidden px-6 py-12 lg:flex-row lg:px-24 text-center lg:text-left">
            {/* Abstract Background Elements */}
            <div className="absolute inset-0 z-[-1] overflow-hidden">
                <div className="absolute top-[-10%] left-[-10%] h-[500px] w-[500px] rounded-full bg-blue-500/10 blur-[100px]" />
                <div className="absolute bottom-[-10%] right-[-10%] h-[500px] w-[500px] rounded-full bg-purple-500/10 blur-[100px]" />
            </div>

            <div className="flex flex-1 flex-col justify-center gap-6 z-10 w-full max-w-2xl">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                >
                    <span className="rounded-full bg-zinc-100 px-3 py-1 text-xs font-medium text-zinc-900 dark:bg-zinc-800 dark:text-zinc-100">
                        Tokyo, Japan 🇯🇵
                    </span>
                </motion.div>

                <motion.h1
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.1 }}
                    className="text-5xl font-black tracking-tight sm:text-7xl lg:text-8xl"
                >
                    Dev & <br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400">
                        Lifestyler.
                    </span>
                </motion.h1>

                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                    className="text-lg text-zinc-600 dark:text-zinc-400 sm:text-xl"
                >
                    Full-Stack Developer based in Tokyo.
                    Crafting digital experiences with a touch of minimalism and efficiency.
                </motion.p>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.3 }}
                    className="flex flex-wrap items-center justify-center lg:justify-start gap-4"
                >
                    <Button size="lg" className="rounded-full gap-2 group">
                        Check Projects
                        <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                    </Button>
                    <div className="flex gap-2">
                        <Button variant="ghost" size="icon" className="rounded-full">
                            <Github className="h-5 w-5" />
                        </Button>
                        <Button variant="ghost" size="icon" className="rounded-full">
                            <Twitter className="h-5 w-5" />
                        </Button>
                    </div>
                </motion.div>
            </div>

            <div className="relative flex-1 flex items-center justify-center lg:justify-end mb-12 lg:mb-0">
                {/* Placeholder for Memoji/Image */}
                <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ duration: 0.8 }}
                    className="relative h-[300px] w-[300px] sm:h-[400px] sm:w-[400px] lg:h-[500px] lg:w-[500px] rounded-full bg-gradient-to-b from-zinc-200 to-white dark:from-zinc-800 dark:to-zinc-950 ring-1 ring-zinc-100 dark:ring-zinc-800 flex items-center justify-center overflow-hidden"
                >
                    <span className="text-zinc-300 dark:text-zinc-600 text-sm font-mono">
                        [Your Image/Memoji Here]
                    </span>
                </motion.div>
            </div>
        </section>
    )
}
