"use client";

import Link from "next/link";

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-stone-900 via-stone-800 to-stone-900 text-white">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_50%_at_50%_-20%,rgba(217,119,6,0.15),transparent)]" />
      <div className="relative mx-auto max-w-6xl px-4 py-24 sm:py-32">
        <div className="mx-auto max-w-3xl text-center">
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl">
            Trouvez votre stage de{" "}
            <span className="text-amber-400">césure</span>
          </h1>
          <p className="mt-6 text-lg text-stone-300 sm:text-xl">
            La plateforme dédiée aux étudiants et jeunes diplômés pour découvrir
            des offres de stages de 6 mois. Inscrivez-vous et accédez au Job Board,
            aux outils et à l&apos;accompagnement.
          </p>
          <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link
              href="/signup"
              className="inline-flex items-center justify-center rounded-lg bg-amber-500 px-6 py-3 text-base font-semibold text-stone-900 shadow-lg hover:bg-amber-400 focus:outline-none focus:ring-2 focus:ring-amber-400 focus:ring-offset-2 focus:ring-offset-stone-900"
            >
              Créer un compte
            </Link>
            <Link
              href="/login"
              className="inline-flex items-center justify-center rounded-lg border-2 border-stone-500 px-6 py-3 text-base font-semibold text-white hover:border-stone-400 hover:bg-stone-800 focus:outline-none focus:ring-2 focus:ring-stone-500 focus:ring-offset-2 focus:ring-offset-stone-900"
            >
              Se connecter
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
