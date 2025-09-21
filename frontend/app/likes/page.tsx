'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useAuthStore } from "@/lib/store";

interface SellerLike {
  id: number;
  buyer_id: number;
  seller_id: number;
  created_at: string;
  seller?: {
    username: string;
    email: string;
  };
}

export default function LikesPage() {
  const [likes, setLikes] = useState<SellerLike[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { token, isAuthenticated } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/auth/login');
      return;
    }

    const fetchLikes = async () => {
      try {
        const response = await fetch('http://localhost:5001/likes/me', {
          headers: { 'Authorization': `Bearer ${token}` },
        });
        if (response.ok) {
          const data = await response.json();
          // For each like, fetch seller details
          const likesWithSellers = await Promise.all(
            data.map(async (like: SellerLike) => {
              try {
                const sellerRes = await fetch(`http://localhost:5001/users/${like.seller_id}`);
                if (sellerRes.ok) {
                  const seller = await sellerRes.json();
                  return { ...like, seller };
                }
              } catch (err) {
                // Ignore errors for individual sellers
              }
              return like;
            })
          );
          setLikes(likesWithSellers);
        } else {
          setError('Failed to load likes');
        }
      } catch (err) {
        setError('Network error');
      } finally {
        setLoading(false);
      }
    };

    fetchLikes();
  }, [token, isAuthenticated, router]);

  const handleUnlike = async (sellerId: number) => {
    try {
      const response = await fetch(`http://localhost:5001/likes/${sellerId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (response.ok) {
        setLikes(likes.filter(like => like.seller_id !== sellerId));
      }
    } catch (err) {
      // Handle error
    }
  };

  if (!isAuthenticated) return null;
  if (loading) return <div className="container mx-auto py-8">Loading...</div>;
  if (error) return <div className="container mx-auto py-8 text-red-500">{error}</div>;

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">Liked Sellers</h1>
      {likes.length === 0 ? (
        <p>No liked sellers yet.</p>
      ) : (
        <div className="grid gap-4">
          {likes.map((like) => (
            <Card key={like.id}>
              <CardHeader>
                <CardTitle>{like.seller?.username || 'Unknown Seller'}</CardTitle>
                <CardDescription>{like.seller?.email}</CardDescription>
              </CardHeader>
              <CardContent>
                <p>Liked on: {new Date(like.created_at).toLocaleDateString()}</p>
                <Button variant="outline" onClick={() => handleUnlike(like.seller_id)}>
                  Unlike
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}