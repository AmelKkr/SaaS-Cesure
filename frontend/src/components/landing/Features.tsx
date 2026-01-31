const features = [
  {
    title: "Job Board",
    description:
      "Offres de stages de 6 mois centralisées. Bientôt disponible : recherche, filtres et candidatures en un clic.",
    comingSoon: true,
  },
  {
    title: "Comptes rendus d'entretien",
    description:
      "Partagez et consultez les retours d'entretien pour mieux vous préparer. Module à venir.",
    comingSoon: true,
  },
  {
    title: "Lettres de motivation & IA",
    description:
      "Aide à la rédaction et personnalisation des lettres. Fonctionnalité prévue dans une prochaine version.",
    comingSoon: true,
  },
  {
    title: "Fiches cabinets & contenu",
    description:
      "Fiches détaillées sur les cabinets et contenus techniques pour vos préparations. À venir.",
    comingSoon: true,
  },
];

export function Features() {
  return (
    <section className="border-t border-stone-200 bg-white py-20">
      <div className="mx-auto max-w-6xl px-4">
        <h2 className="text-center text-3xl font-bold text-stone-900 sm:text-4xl">
          Tout pour réussir votre césure
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-center text-stone-600">
          Une plateforme modulaire pensée pour les étudiants et jeunes diplômés.
          Le core est en place ; les modules métier arrivent progressivement.
        </p>
        <div className="mt-16 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((f) => (
            <div
              key={f.title}
              className="rounded-xl border border-stone-200 bg-stone-50 p-6 shadow-sm"
            >
              <div className="flex items-center gap-2">
                <h3 className="text-lg font-semibold text-stone-900">
                  {f.title}
                </h3>
                {f.comingSoon && (
                  <span className="rounded-full bg-amber-100 px-2 py-0.5 text-xs font-medium text-amber-800">
                    Bientôt
                  </span>
                )}
              </div>
              <p className="mt-2 text-sm text-stone-600">{f.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
