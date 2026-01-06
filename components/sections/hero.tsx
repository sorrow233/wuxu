"use client"
/* eslint-disable @typescript-eslint/no-explicit-any */

import { motion } from "framer-motion"

export function Hero({ dict }: { dict: any }) {
    if (!dict) return null;

    return (
        <section className="relative w-full h-screen min-h-[600px] bg-[#EAE4D9] overflow-hidden">
            {/* Background Image Container */}
            <div className="absolute inset-0 z-0">
                <motion.div
                    initial={{ opacity: 0, scale: 1.05 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 1.2, ease: "easeOut" }}
                    className="h-full w-full"
                >
                    <img
                        src="/images/hero_cover.png"
                        alt="Hero Cover"
                        className="h-full w-full object-cover object-center"
                    />
                </motion.div>
            </div>

            {/* Overlay Content */}
            <div className="relative z-10 w-full h-full p-8 md:p-12 flex flex-col justify-between pointer-events-none">
                {/* Logo Area */}
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.5 }}
                    className="flex items-start"
                >
                    <h1 className="text-3xl font-serif tracking-tight text-[#2D2D2D] pointer-events-auto">
                        wuxu <br />
                        <span className="text-lg font-sans font-light tracking-widest uppercase opacity-70">design</span>
                    </h1>
                </motion.div>

                {/* Bottom Scroll Indicator (Optional) */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.8, delay: 1 }}
                    className="absolute bottom-12 right-12 hidden md:flex items-center gap-4 origin-right rotate-90"
                >
                    <span className="text-xs tracking-[0.2em] uppercase text-[#2D2D2D]">Scroll</span>
                    <div className="w-12 h-px bg-[#2D2D2D]"></div>
                </motion.div>
            </div>
        </section>
    )
}
