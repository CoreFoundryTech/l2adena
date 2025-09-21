'use client';

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { LanguageSelector } from "@/components/LanguageSelector";
import { useAuthStore } from "@/lib/store";
import { useTranslation } from 'react-i18next';

export default function Home() {
  const { isAuthenticated, logout, user } = useAuthStore();
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <header className="container mx-auto px-4 py-6">
        <nav className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">L2 Adena Marketplace</h1>
          <div className="flex items-center space-x-4">
            <LanguageSelector />
            {isAuthenticated ? (
              <>
                <span>{t('nav.welcome', { username: user?.username })}</span>
                <Link href="/profile">
                  <Button variant="outline">{t('nav.profile')}</Button>
                </Link>
                <Link href="/purchase-history">
                  <Button variant="outline">{t('nav.purchaseHistory')}</Button>
                </Link>
                <Link href="/likes">
                  <Button variant="outline">{t('nav.likes')}</Button>
                </Link>
                <Link href="/premium">
                  <Button variant="outline">{t('nav.premium')}</Button>
                </Link>
                <Button onClick={logout}>{t('nav.logout')}</Button>
              </>
            ) : (
              <>
                <Link href="/auth/login">
                  <Button variant="outline">{t('nav.login')}</Button>
                </Link>
                <Link href="/auth/register">
                  <Button>{t('nav.register')}</Button>
                </Link>
              </>
            )}
          </div>
        </nav>
      </header>

      <main className="container mx-auto px-4 py-16 text-center">
        <h2 className="text-4xl font-bold text-gray-900 mb-4">
          {t('home.title')}
        </h2>
        <p className="text-xl text-gray-600 mb-8">
          {t('home.subtitle')}
        </p>
        <div className="space-x-4">
          <Link href="/listings">
            <Button size="lg">{t('home.browseListings')}</Button>
          </Link>
          {isAuthenticated && (
            <Link href="/profile">
              <Button variant="outline" size="lg">{t('home.viewProfile')}</Button>
            </Link>
          )}
        </div>
      </main>
    </div>
  );
}
