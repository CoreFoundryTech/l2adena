import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

interface ProfileCardProps {
  name: string;
  email: string;
  avatar?: string;
  bio?: string;
  likesCount?: number;
  averageRating?: number;
  reviewCount?: number;
  isVerified?: boolean;
  isOwnProfile?: boolean;
  onEdit?: () => void;
  onLike?: () => void;
  isLiked?: boolean;
}

export function ProfileCard({
  name,
  email,
  avatar,
  bio,
  likesCount = 0,
  averageRating = 0,
  reviewCount = 0,
  isVerified = false,
  isOwnProfile = false,
  onEdit,
  onLike,
  isLiked = false
}: ProfileCardProps) {
  return (
    <Card className="w-full max-w-md">
      <CardHeader className="text-center">
        <Avatar className="w-20 h-20 mx-auto">
          <AvatarImage src={avatar} alt={name} />
          <AvatarFallback>{name.charAt(0)}</AvatarFallback>
        </Avatar>
        <div className="flex items-center justify-center gap-2">
          <CardTitle>{name}</CardTitle>
          {isVerified && <Badge variant="default" className="bg-blue-500">Verificado</Badge>}
        </div>
        <CardDescription>{email}</CardDescription>
        <div className="flex justify-center gap-2 mt-2">
          <Badge variant="secondary">Likes: {likesCount}</Badge>
          <Badge variant="outline">Rating: {averageRating.toFixed(1)} ({reviewCount})</Badge>
        </div>
      </CardHeader>
      <CardContent>
        {bio && <p className="text-sm text-muted-foreground mb-4">{bio}</p>}
        <div className="flex gap-2">
          {isOwnProfile ? (
            <Button className="flex-1" onClick={onEdit}>Edit Profile</Button>
          ) : (
            <>
              <Button
                variant={isLiked ? "secondary" : "default"}
                className="flex-1"
                onClick={onLike}
              >
                {isLiked ? 'Unlike' : 'Like'}
              </Button>
            </>
          )}
        </div>
      </CardContent>
    </Card>
  );
}