"use client";

import Link from "next/link";
import { SignupForm } from "@/components/auth/SignupForm";

export default function SignupPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-stone-50 px-4">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <Link href="/" className="text-2xl font-semibold text-stone-900">
            Césure
          </Link>
          <h1 className="mt-6 text-2xl font-bold text-stone-900">
            Inscription
          </h1>
          <p className="mt-2 text-sm text-stone-600">
            Créez votre compte pour accéder aux offres de stages
          </p>
        </div>
        <SignupForm />
        <p className="text-center text-sm text-stone-600">
          Déjà un compte ?{" "}
          <Link href="/login" className="font-medium text-amber-700 hover:underline">
            Se connecter
          </Link>
        </p>
      </div>
    </div>
  );
}
