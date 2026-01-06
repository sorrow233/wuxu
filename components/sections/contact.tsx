"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Mail } from "lucide-react"

export function Contact({ dict }: { dict: any }) {
    if (!dict) return null;

    return (
        <section className="w-full px-6 py-24 lg:px-24 bg-zinc-900 text-white overflow-hidden relative">
            {/* Background Decoration */}
            <div className="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-zinc-700 to-transparent" />

            <div className="mx-auto max-w-2xl text-center relative z-10">
                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5 }}
                >
                    <h2 className="text-3xl font-bold tracking-tight sm:text-4xl mb-6">
                        {dict.title}
                    </h2>
                    <p className="text-zinc-400 mb-8 text-lg">
                        {dict.description}
                    </p>
                    <Button size="lg" className="rounded-full px-8 py-6 text-lg bg-white text-black hover:bg-zinc-200">
                        <Mail className="mr-2 h-5 w-5" /> {dict.cta}
                    </Button>
                </motion.div>
            </div>
        </section>
    )
}
