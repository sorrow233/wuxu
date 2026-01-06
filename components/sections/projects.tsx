"use client"
/* eslint-disable @typescript-eslint/no-explicit-any */

import { motion } from "framer-motion"

export function Projects({ dict, common }: { dict: any, common: any }) {
    if (!dict) return null;
    const projects = dict.list;

    return (
        <section className="w-full px-6 py-32 lg:px-24 bg-[#EAE4D9]">
            <div className="mx-auto max-w-7xl">
                {/* Section Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6 }}
                    className="flex flex-col items-center justify-center mb-24"
                >
                    <h2 className="text-4xl font-serif text-[#2D2D2D] mb-4">Works</h2>
                    <div className="h-px w-24 bg-[#2D2D2D]/20"></div>
                </motion.div>

                {/* Projects Grid */}
                <div className="grid gap-x-8 gap-y-8 sm:grid-cols-2">
                    {projects.map((project: any, index: number) => (
                        <motion.div
                            key={project.title}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                            className="group relative cursor-pointer block"
                        >
                            <a href={project.links.demo || "#"} target="_blank" rel="noopener noreferrer" className="block relative aspect-[4/3] overflow-hidden">
                                {/* Image */}
                                <img
                                    src={project.image}
                                    alt={project.title}
                                    className="h-full w-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
                                />

                                {/* Overlay */}
                                <div className="absolute inset-0 bg-[#2D2D2D]/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col items-center justify-center text-center p-6 backdrop-blur-[2px]">
                                    <h3 className="text-2xl font-serif text-[#FBF9F4] mb-2 translate-y-4 group-hover:translate-y-0 transition-transform duration-500 delay-75">
                                        {project.title}
                                    </h3>
                                    <p className="text-sm font-sans tracking-widest uppercase text-[#FBF9F4]/80 translate-y-4 group-hover:translate-y-0 transition-transform duration-500 delay-100">
                                        {project.tags[0]} / {common.demo}
                                    </p>
                                </div>
                            </a>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    )
}
