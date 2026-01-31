"use client";

import Link from "next/link";

export function Pricing() {
  return (
    <section className="border-t border-stone-200 bg-stone-50 py-20">
      <div className="mx-auto max-w-6xl px-4">
        <h2 className="text-center text-3xl font-bold text-stone-900 sm:text-4xl">
          Tarifs simples
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-center text-stone-600">
          Un abonnement pour accéder à l&apos;ensemble des modules (Job Board,
          fiches, outils) dès leur mise en ligne.
        </p>
        <div className="mx-auto mt-12 max-w-md">
          <div className="rounded-2xl border border-stone-200 bg-white p-8 shadow-lg">
            <h3 className="text-xl font-semibold text-stone-900">
              Césure Pro
            </h3>
            <p className="mt-2 text-sm text-stone-600">
              Accès complet aux stages 6 mois et aux outils d&apos;accompagnement.
            </p>
            <div className="mt-6">
              <span className="text-3xl font-bold text-stone-900">
                Sur devis
              </span>
            </div>
            <Link
              href="/signup"
              className="mt-6 block w-full rounded-lg bg-amber-600 py-3 text-center font-semibold text-white hover:bg-amber-700"
            >
              S&apos;inscrire et souscrire
            </Link>
            <p className="mt-4 text-center text-xs text-stone-500">
              Paiement sécurisé via Stripe. Gestion de l&apos;abonnement depuis
              votre tableau de bord.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
