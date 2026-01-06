"use client"

import { motion } from "framer-motion"

const skills = [
    "JavaScript", "TypeScript", "React", "Next.js",
    "Node.js", "Python", "Tailwind CSS", "Framer Motion", "Git", "Docker"
]

export function About({ dict }: { dict: any }) {
    if (!dict) return null;

    return (
        <section className="w-full px-6 py-24 lg:px-24 bg-white dark:bg-zinc-950">
            <div className="mx-auto max-w-4xl">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5 }}
                    className="grid gap-12 lg:grid-cols-2 lg:gap-8 items-start"
                >
                    <div className="space-y-6">
                        <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">{dict.title}</h2>
                        <div className="space-y-4 text-zinc-600 dark:text-zinc-400">
                            <p>
                                {dict.description1}
                                <span className="font-semibold text-zinc-900 dark:text-zinc-100"> {dict.description2}</span>.
                            </p>
                            <p>
                                {dict.description3}
                            </p>
                            <p>
                                {dict.description4}
                            </p>
                        </div>
                    </div>

                    <div className="p-6 rounded-2xl bg-zinc-50 dark:bg-zinc-900/50 border border-zinc-100 dark:border-zinc-800">
                        <h3 className="text-xl font-semibold mb-6">{dict.techStack}</h3>
                        <div className="flex flex-wrap gap-2">
                            {skills.map((skill) => (
                                <span
                                    key={skill}
                                    className="px-3 py-1 text-sm bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-full shadow-sm"
                                >
                                    {skill}
                                </span>
                            ))}
                        </div>
                    </div>
                </motion.div>
            </div>
        </section>
    )
}
