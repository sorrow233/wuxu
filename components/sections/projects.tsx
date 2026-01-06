"use client"

import { motion } from "framer-motion"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Github, ExternalLink } from "lucide-react"

const projects = [
    {
        title: "Metro Nav",
        description: "Real-time navigation app for the subway system aimed at tourists.",
        tags: ["Next.js", "Leaflet", "OpenData"],
        links: { github: "#", demo: "#" },
    },
    {
        title: "Kanji Flashcards",
        description: "SRS-based flashcard app for mastering JLPT N2/N1 kanji.",
        tags: ["React", "Firebase", "PWA"],
        links: { github: "#", demo: "#" },
    },
    {
        title: "Personal Portfolio",
        description: "The website you are looking at right now. Built with modern tech.",
        tags: ["Next.js", "Tailwind", "Framer Motion"],
        links: { github: "#", demo: "#" },
    },
]

export function Projects({ dict }: { dict: any }) {
    if (!dict) return null;

    return (
        <section className="w-full px-6 py-24 lg:px-24 bg-zinc-50/50 dark:bg-zinc-900/50">
            <div className="mx-auto max-w-5xl">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5 }}
                    className="mb-12 text-center lg:text-left"
                >
                    <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">{dict.title}</h2>
                    <p className="mt-4 text-zinc-500 dark:text-zinc-400">
                        {dict.description}
                    </p>
                </motion.div>

                <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
                    {projects.map((project, index) => (
                        <motion.div
                            key={project.title}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                        >
                            <Card className="h-full flex flex-col hover:shadow-lg transition-shadow duration-300">
                                <CardHeader>
                                    <CardTitle>{project.title}</CardTitle>
                                    <CardDescription className="mt-2 text-xs text-zinc-400">
                                        {project.tags.join(" • ")}
                                    </CardDescription>
                                </CardHeader>
                                <CardContent className="flex-1">
                                    <p className="text-sm text-zinc-600 dark:text-zinc-300">
                                        {project.description}
                                    </p>
                                </CardContent>
                                <CardFooter className="flex gap-2">
                                    <Button variant="outline" size="sm" className="w-full gap-2">
                                        <Github className="h-4 w-4" /> Code
                                    </Button>
                                    <Button size="sm" className="w-full gap-2">
                                        <ExternalLink className="h-4 w-4" /> Demo
                                    </Button>
                                </CardFooter>
                            </Card>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    )
}
