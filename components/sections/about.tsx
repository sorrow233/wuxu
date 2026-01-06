"use client"

import { motion } from "framer-motion"

const skills = [
    "JavaScript", "TypeScript", "React", "Next.js",
    "Node.js", "Python", "Tailwind CSS", "Framer Motion", "Git", "Docker"
]

export function About({ dict }: { dict: any }) {
    if (!dict) return null;

    return (
        <section className="w-full px-6 py-32 lg:px-24 bg-zinc-50 dark:bg-zinc-950/50">
            <div className="mx-auto max-w-6xl">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6 }}
                    className="grid gap-16 lg:grid-cols-[1fr,1.2fr] items-start"
                >
                    <div className="space-y-8 sticky top-24">
                        <div className="space-y-2">
                            <span className="text-sm font-medium tracking-widest text-primary uppercase">About Me</span>
                            <h2 className="text-4xl font-light tracking-tight text-foreground">{dict.title}</h2>
                        </div>

                        <div className="p-8 rounded-2xl bg-white dark:bg-zinc-900/50 border border-zinc-100 dark:border-zinc-800 shadow-sm">
                            <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-6">{dict.techStack}</h3>
                            <div className="flex flex-wrap gap-2">
                                {skills.map((skill) => (
                                    <span
                                        key={skill}
                                        className="px-4 py-2 text-sm bg-secondary/50 text-secondary-foreground border border-transparent hover:border-zinc-300 dark:hover:border-zinc-700 rounded-lg transition-colors cursor-default"
                                    >
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        </div>
                    </div>

                    <div className="space-y-8 text-lg leading-loose text-muted-foreground font-light">
                        <p className="first-letter:text-5xl first-letter:font-bold first-letter:text-primary first-letter:mr-3 float-left">
                            {dict.description1.charAt(0)}
                        </p>
                        <p>
                            {dict.description1.slice(1)}
                            <span className="font-medium text-foreground"> {dict.description2}</span>.
                        </p>
                        <p>
                            {dict.description3}
                        </p>
                        <p>
                            {dict.description4}
                        </p>

                        <div className="pt-8 grid grid-cols-2 gap-8 border-t border-zinc-200 dark:border-zinc-800">
                            {/*  Stats or extra info could go here for "Rich" feel */}
                            <div>
                                <span className="block text-3xl font-bold text-foreground">3+</span>
                                <span className="text-sm text-muted-foreground">Years Experience</span>
                            </div>
                            <div>
                                <span className="block text-3xl font-bold text-foreground">15+</span>
                                <span className="text-sm text-muted-foreground">Projects Completed</span>
                            </div>
                        </div>
                    </div>
                </motion.div>
            </div>
        </section>
    )
}
