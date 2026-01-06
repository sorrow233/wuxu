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
        <section className="w-full px-6 py-32 lg:px-24 bg-background">
            <div className="mx-auto max-w-7xl">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6 }}
                    className="mb-20 flex flex-col items-start gap-4"
                >
                    <span className="text-sm font-medium tracking-widest text-primary uppercase">{common.works}</span>
                    <h2 className="text-4xl font-light tracking-tight sm:text-5xl text-foreground">{dict.title}</h2>
                    <p className="max-w-2xl text-lg text-muted-foreground font-light">
                        {dict.description}
                    </p>
                </motion.div>

                <div className="grid gap-12 sm:grid-cols-2 lg:grid-cols-3">
                    {projects.map((project: any, index: number) => (
                        <motion.div
                            key={project.title}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                            className="group"
                        >
                            <Card className="h-full flex flex-col border border-border bg-card/50 hover:bg-card transition-all duration-300 hover:-translate-y-1 hover:shadow-xl rounded-xl overflow-hidden hover:border-primary/20">
                                <CardHeader className="pb-4">
                                    <div className="flex justify-between items-start">
                                        <CardTitle className="text-xl font-medium tracking-tight">{project.title}</CardTitle>
                                        <ArrowUpRight className="h-5 w-5 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                                    </div>
                                    <CardDescription className="flex flex-wrap gap-2 mt-3">
                                        {project.tags.map((tag: string) => (
                                            <span key={tag} className="text-xs px-2 py-1 bg-secondary rounded-md text-secondary-foreground font-medium">
                                                {tag}
                                            </span>
                                        ))}
                                    </CardDescription>
                                </CardHeader>
                                <CardContent className="flex-1">
                                    <p className="text-sm leading-relaxed text-muted-foreground">
                                        {project.description}
                                    </p>
                                </CardContent>
                                <CardFooter className="flex gap-4 pt-6 border-t border-border/50">
                                    <a href={project.links.github} className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors flex items-center gap-2">
                                        <Github className="h-4 w-4" /> {common.code}
                                    </a>
                                    <a href={project.links.demo} className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors flex items-center gap-2">
                                        <ExternalLink className="h-4 w-4" /> {common.demo}
                                    </a>
                                </CardFooter>
                            </Card>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    )
}
