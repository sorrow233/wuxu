"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { ArrowRight, Github, MapPin, Twitter } from "lucide-react"

export function Hero({ dict }: { dict: any }) {
    if (!dict) return null;

    return (
        <section className="relative flex min-h-[90vh] flex-col-reverse items-center justify-center overflow-hidden px-6 py-12 lg:flex-row lg:px-24 text-center lg:text-left">
            {/* Abstract Background Elements - Vibrancy */}
            <div className="absolute inset-0 z-[-1] overflow-hidden">
                <div className="absolute top-[-10%] left-[-10%] h-[500px] w-[500px] rounded-full bg-primary/10 blur-[100px]" />
                <div className="absolute bottom-[-10%] right-[-10%] h-[500px] w-[500px] rounded-full bg-secondary/10 blur-[100px]" />
            </div>

            <div className="flex flex-1 flex-col justify-center gap-6 z-10 w-full max-w-2xl">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                    className="flex items-center justify-center lg:justify-start gap-2"
                >
                </motion.div>

                <motion.h1
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.1 }}
                    className="text-5xl font-black tracking-tight sm:text-7xl lg:text-8xl"
                >
                    {dict.titleStart} <br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
                        {dict.titleEnd}
                    </span>
                </motion.h1>

                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                    className="text-lg text-muted-foreground sm:text-xl"
                >
                    {dict.description}
                </motion.p>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.3 }}
                    className="flex flex-wrap items-center justify-center lg:justify-start gap-4"
                >
                    <Button size="lg" className="rounded-full gap-2 group bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg hover:shadow-xl transition-all">
                        {dict.ctaProject}
                        <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                    </Button>
                    <div className="flex gap-2">
                        <Button variant="ghost" size="icon" className="rounded-full hover:bg-accent hover:text-accent-foreground transition-colors">
                            <Github className="h-5 w-5" />
                        </Button>
                        <Button variant="ghost" size="icon" className="rounded-full hover:bg-accent hover:text-accent-foreground transition-colors">
                            <Twitter className="h-5 w-5" />
                        </Button>
                    </div>
                </motion.div>
            </div>

            <div className="relative flex-1 flex items-center justify-center lg:justify-end mb-12 lg:mb-0">
                {/* Placeholder for Memoji/Image - Kept simple but vibrant */}
                <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ duration: 0.8 }}
                    className="relative h-[300px] w-[300px] sm:h-[400px] sm:w-[400px] lg:h-[500px] lg:w-[500px] rounded-full bg-gradient-to-tr from-primary/20 via-white to-secondary/20 dark:from-primary/10 dark:to-secondary/10 ring-1 ring-border flex items-center justify-center overflow-hidden shadow-2xl"
                >
                    <span className="text-muted-foreground text-sm font-mono">
                        [Your Image/Memoji Here]
                    </span>
                </motion.div>
            </div>
        </section>
    )
}
