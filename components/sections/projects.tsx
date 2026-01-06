"use client"
/* eslint-disable @typescript-eslint/no-explicit-any */

import { motion } from "framer-motion"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Github, ExternalLink, ArrowUpRight } from "lucide-react"

export function Projects({ dict, common }: { dict: any, common: any }) {
    if (!dict) return null;
    const projects = dict.list;

    return (
        <section className="w-full px-6 py-32 lg:px-24 bg-[#fbf9f4]">
            <div className="mx-auto max-w-7xl">
                {/* Section Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6 }}
                    className="flex flex-col items-center justify-center mb-24"
                >
                    <h2 className="text-4xl font-serif text-foreground mb-4">Works</h2>
                    <div className="h-px w-24 bg-foreground/20"></div>
                    <p className="mt-4 text-muted-foreground font-light text-center max-w-lg">
                        {dict.description}
                    </p>
                </motion.div>

                {/* Projects Grid */}
                <div className="grid gap-x-8 gap-y-16 sm:grid-cols-2">
                    {projects.map((project: any, index: number) => (
                        <motion.div
                            key={project.title}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                            className="group cursor-pointer"
                        >
                            <div className="relative overflow-hidden mb-6">
                                <a href={project.links.demo || "#"} target="_blank" rel="noopener noreferrer" className="block">
                                    <div className="aspect-[4/3] overflow-hidden bg-secondary/20">
                                        <img
                                            src={project.image}
                                            alt={project.title}
                                            className="h-full w-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
                                        />
                                    </div>
                                </a>
                            </div>

                            <div className="flex flex-col items-center text-center">
                                <h3 className="text-xl font-medium tracking-wide text-foreground mb-2">
                                    {project.title}
                                </h3>
                                <p className="text-sm text-muted-foreground font-light leading-relaxed max-w-md mb-4">
                                    {project.description}
                                </p>
                                <div className="flex flex-wrap gap-2 justify-center mb-4">
                                    {project.tags.map((tag: string) => (
                                        <span key={tag} className="text-xs text-muted-foreground/60 uppercase tracking-wider">
                                            {tag}
                                        </span>
                                    ))}
                                </div>
                                <div className="flex gap-4 opacity-0 transform translate-y-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-y-0">
                                    <a href={project.links.github} className="text-xs font-medium text-foreground hover:text-primary/70 transition-colors uppercase tracking-widest border-b border-transparent hover:border-foreground">
                                        {common.code}
                                    </a>
                                    <a href={project.links.demo} className="text-xs font-medium text-foreground hover:text-primary/70 transition-colors uppercase tracking-widest border-b border-transparent hover:border-foreground">
                                        {common.demo}
                                    </a>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    )
}
