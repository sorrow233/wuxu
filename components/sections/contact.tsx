"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Mail } from "lucide-react"

export function Contact({ dict }: { dict: any }) {
    if (!dict) return null;

    return (
        <section className="w-full px-6 py-32 lg:px-24 bg-foreground text-background overflow-hidden relative">

            <div className="mx-auto max-w-4xl text-center relative z-10 flex flex-col items-center">
                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6 }}
                    className="space-y-10"
                >
                    <div className="space-y-4">
                        <span className="text-sm font-medium tracking-widest text-zinc-400 uppercase">Contact</span>
                        <h2 className="text-5xl font-light tracking-tight sm:text-6xl text-background">
                            {dict.title}
                        </h2>
                    </div>

                    <p className="text-zinc-400 max-w-xl mx-auto text-lg font-light leading-relaxed">
                        {dict.description}
                    </p>

                    <Button size="lg" className="rounded-full px-10 py-8 text-lg bg-background text-foreground hover:bg-zinc-200 hover:scale-105 transition-all duration-300 shadow-xl">
                        <Mail className="mr-3 h-5 w-5" /> {dict.cta}
                    </Button>
                </motion.div>
            </div>

            {/* Subtle Texture/Grain could go here if using images, but keeping css only for now */}
            <div className="absolute inset-0 opacity-5 pointer-events-none bg-[url('https://grainy-gradients.vercel.app/noise.svg')] brightness-100 contrast-150"></div>
        </section>
    )
}
