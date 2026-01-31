"use client";

import { useAuth } from "@/hooks/useAuth";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

export default function DashboardPage() {
  const { user } = useAuth();
  const searchParams = useSearchParams();
  const [checkoutStatus, setCheckoutStatus] = useState<string | null>(null);

  useEffect(() => {
    const status = searchParams.get("checkout");
    if (status) setCheckoutStatus(status);
  }, [searchParams]);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-stone-900">
          Tableau de bord
        </h1>
        <p className="mt-1 text-stone-600">
          Bienvenue, {user?.full_name || user?.email}.
        </p>
      </div>

      {checkoutStatus === "success" && (
        <div className="rounded-lg border border-green-200 bg-green-50 p-4 text-green-800">
          Votre abonnement a bien été enregistré.
        </div>
      )}
      {checkoutStatus === "cancel" && (
        <div className="rounded-lg border border-amber-200 bg-amber-50 p-4 text-amber-800">
          Paiement annulé. Vous pouvez réessayer quand vous le souhaitez.
        </div>
      )}

      <div className="rounded-xl border border-stone-200 bg-white p-6 shadow-sm">
        <h2 className="text-lg font-semibold text-stone-900">
          Votre espace
        </h2>
        <p className="mt-2 text-sm text-stone-600">
          Le Job Board, les comptes rendus d&apos;entretien et les autres modules
          métier seront disponibles ici après connexion à votre abonnement.
        </p>
      </div>
    </div>
  );
}
