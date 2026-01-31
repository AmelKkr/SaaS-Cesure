"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";

export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, loading, logout } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-stone-50">
        <div className="animate-pulse text-stone-500">Chargement...</div>
      </div>
    );
  }

  if (!user) {
    router.replace("/login");
    return null;
  }

  return (
    <div className="min-h-screen bg-stone-50">
      <header className="border-b border-stone-200 bg-white">
        <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
          <Link href="/dashboard" className="text-lg font-semibold text-stone-900">
            Césure
          </Link>
          <nav className="flex items-center gap-6">
            <Link
              href="/dashboard"
              className={`text-sm font-medium ${
                pathname === "/dashboard"
                  ? "text-amber-700"
                  : "text-stone-600 hover:text-stone-900"
              }`}
            >
              Tableau de bord
            </Link>
            <span className="text-sm text-stone-500">
              {user.email}
            </span>
            <button
              type="button"
              onClick={() => logout()}
              className="text-sm font-medium text-stone-600 hover:text-stone-900"
            >
              Déconnexion
            </button>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
    </div>
  );
}
