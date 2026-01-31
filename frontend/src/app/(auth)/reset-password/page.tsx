"use client";

import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { ResetPasswordForm } from "@/components/auth/ResetPasswordForm";

export default function ResetPasswordPage() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token") ?? "";

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-stone-50 px-4">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <Link href="/" className="text-2xl font-semibold text-stone-900">
            Césure
          </Link>
          <h1 className="mt-6 text-2xl font-bold text-stone-900">
            Nouveau mot de passe
          </h1>
          <p className="mt-2 text-sm text-stone-600">
            Choisissez un nouveau mot de passe sécurisé
          </p>
        </div>
        {token ? (
          <ResetPasswordForm token={token} />
        ) : (
          <p className="text-center text-stone-600">
            Lien invalide ou expiré.{" "}
            <Link href="/forgot-password" className="font-medium text-amber-700 hover:underline">
              Redemander un lien
            </Link>
          </p>
        )}
        <p className="text-center text-sm text-stone-600">
          <Link href="/login" className="font-medium text-amber-700 hover:underline">
            Retour à la connexion
          </Link>
        </p>
      </div>
    </div>
  );
}
