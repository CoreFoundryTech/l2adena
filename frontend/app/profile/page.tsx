'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ProfileCard } from "@/components/ProfileCard";
import { useAuthStore } from "@/lib/store";

interface ProfileData {
  user: {
    id: number;
    username: string;
    email: string;
    is_verified: boolean;
  };
  profile?: {
    description?: string;
    server_list?: string;
  };
  likesCount: number;
  averageRating: number;
  reviewCount: number;
}

export default function ProfilePage() {
  const [profileData, setProfileData] = useState<ProfileData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user, token, isAuthenticated } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/auth/login');
      return;
    }

    const fetchProfile = async () => {
      try {
        const [profileRes, likesRes, reputationRes] = await Promise.all([
          fetch('http://localhost:5001/profiles/me', {
            headers: { 'Authorization': `Bearer ${token}` },
          }),
          fetch(`http://localhost:5001/users/${user!.id}/likes-count`),
          fetch(`http://localhost:5001/users/${user!.id}/reputation`),
        ]);

        const profile = profileRes.ok ? await profileRes.json() : null;
        const likes = likesRes.ok ? await likesRes.json() : { likes_count: 0 };
        const reputation = reputationRes.ok ? await reputationRes.json() : { average_rating: 0, review_count: 0 };

        setProfileData({
          user: user!,
          profile,
          likesCount: likes.likes_count,
          averageRating: reputation.average_rating,
          reviewCount: reputation.review_count,
        });
      } catch (err) {
        setError('Failed to load profile');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [user, token, isAuthenticated, router]);

  if (!isAuthenticated) return null;
  if (loading) return <div className="container mx-auto py-8">Loading...</div>;
  if (error) return <div className="container mx-auto py-8 text-red-500">{error}</div>;
  if (!profileData) return <div className="container mx-auto py-8">No profile data</div>;

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">My Profile</h1>
      <ProfileCard
        name={profileData.user.username}
        email={profileData.user.email}
        bio={profileData.profile?.description}
        likesCount={profileData.likesCount}
        averageRating={profileData.averageRating}
        reviewCount={profileData.reviewCount}
        isVerified={profileData.user.is_verified}
        isOwnProfile={true}
        onEdit={() => router.push('/profile/edit')}
      />
    </div>
  );
}