import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t border-stone-200 bg-stone-900 py-12 text-stone-300">
      <div className="mx-auto max-w-6xl px-4">
        <div className="flex flex-col items-center justify-between gap-6 sm:flex-row">
          <Link href="/" className="text-lg font-semibold text-white">
            Césure
          </Link>
          <nav className="flex gap-6">
            <Link
              href="/login"
              className="text-sm hover:text-white"
            >
              Connexion
            </Link>
            <Link
              href="/signup"
              className="text-sm hover:text-white"
            >
              Inscription
            </Link>
          </nav>
        </div>
        <p className="mt-8 text-center text-sm text-stone-500">
          © {new Date().getFullYear()} Césure. Stages de 6 mois pour étudiants et jeunes diplômés.
        </p>
      </div>
    </footer>
  );
}
