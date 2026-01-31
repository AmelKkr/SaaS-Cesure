import type { Metadata } from "next";
import "@/styles/globals.css";

export const metadata: Metadata = {
  title: "Césure – Stages de 6 mois pour étudiants et jeunes diplômés",
  description:
    "Trouvez votre stage de césure. Plateforme dédiée aux étudiants et jeunes diplômés pour découvrir des offres de stages de 6 mois.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
