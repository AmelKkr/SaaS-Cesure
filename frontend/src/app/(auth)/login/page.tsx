"use client";

import Link from "next/link";
import { LoginForm } from "@/components/auth/LoginForm";

export default function LoginPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-stone-50 px-4">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <Link href="/" className="text-2xl font-semibold text-stone-900">
            Césure
          </Link>
          <h1 className="mt-6 text-2xl font-bold text-stone-900">
            Connexion
          </h1>
          <p className="mt-2 text-sm text-stone-600">
            Accédez à votre espace stages de 6 mois
          </p>
        </div>
        <LoginForm />
        <p className="text-center text-sm text-stone-600">
          Pas encore de compte ?{" "}
          <Link href="/signup" className="font-medium text-amber-700 hover:underline">
            S&apos;inscrire
          </Link>
        </p>
      </div>
    </div>
  );
}
