"use client";

import Link from "next/link";
import { ForgotPasswordForm } from "@/components/auth/ForgotPasswordForm";

export default function ForgotPasswordPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-stone-50 px-4">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <Link href="/" className="text-2xl font-semibold text-stone-900">
            Césure
          </Link>
          <h1 className="mt-6 text-2xl font-bold text-stone-900">
            Mot de passe oublié
          </h1>
          <p className="mt-2 text-sm text-stone-600">
            Entrez votre email pour recevoir un lien de réinitialisation
          </p>
        </div>
        <ForgotPasswordForm />
        <p className="text-center text-sm text-stone-600">
          <Link href="/login" className="font-medium text-amber-700 hover:underline">
            Retour à la connexion
          </Link>
        </p>
      </div>
    </div>
  );
}
