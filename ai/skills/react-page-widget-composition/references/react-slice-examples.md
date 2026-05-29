# React Slice Examples

Use these examples when implementing `react-page-widget-composition`.

## Page Composition

Pages own layout and pass positioning classes into stateless components and widgets.

```tsx
import "./profile-page.css";

import { ProfileHeader } from "../../components/profile-header/profile-header";
import { ProfileMain } from "../../components/profile-main/profile-main";
import { ProfileShell } from "../../components/profile-shell/profile-shell";
import { SubscriptionEntry } from "../../components/subscription-entry/subscription-entry";
import { ProfileStatsWidget } from "../../widgets/profile-stats/profile-stats.widget";
import { SaveProfileWidget } from "../../widgets/save-profile/save-profile.widget";
import { SubscriptionsListWidget } from "../../widgets/subscriptions-list/subscriptions-list.widget";

export const ProfilePage = () => {
  return (
    <ProfileShell className="profile-page">
      <ProfileHeader className="profile-page__header" />

      <ProfileMain className="profile-page__main">
        <ProfileStatsWidget className="profile-page__stats" />
        <SaveProfileWidget className="profile-page__actions" />

        <SubscriptionsListWidget className="profile-page__subscriptions">
          {({ subscriptions }) =>
            subscriptions.map((subscription) => (
              <SubscriptionEntry
                key={subscription.id}
                subscription={subscription}
              />
            ))
          }
        </SubscriptionsListWidget>
      </ProfileMain>
    </ProfileShell>
  );
};
```

```css
.profile-page {
  min-height: 100%;
}

.profile-page__main {
  display: grid;
  gap: 24px;
  grid-template-columns: minmax(0, 1fr) 320px;
}

.profile-page__stats {
  grid-column: 2;
}

.profile-page__subscriptions {
  grid-column: 1 / -1;
}
```

## Render-Prop Widget Contract

Use render-prop children only when the page should control item rendering while the widget owns loading/query orchestration.

```tsx
import type { ReactNode } from "react";
import { useQuery } from "@tanstack/react-query";

import { subscriptionsQuery } from "../../store/queries/subscriptions-query";

export type Subscription = {
  id: string;
  name: string;
};

export type SubscriptionsListWidgetProps = {
  children: (state: { subscriptions: Subscription[] }) => ReactNode;
  className?: string;
};

export const SubscriptionsListWidget = ({
  children,
  className,
}: SubscriptionsListWidgetProps) => {
  const subscriptionsQueryResult = useQuery(subscriptionsQuery());

  if (subscriptionsQueryResult.isLoading) {
    return <div className={className}>Loading...</div>;
  }

  return (
    <section className={className}>
      {children({ subscriptions: subscriptionsQueryResult.data ?? [] })}
    </section>
  );
};
```

## Widget-Owned Stateless Component

```text
widgets/
  profile-stats/
    profile-stats.tsx
    profile-stats.css
    profile-stats.widget.tsx
    profile-stats.widget.stories.tsx
```

```tsx
import "./profile-stats.css";

export type ProfileStatsProps = {
  className?: string;
  error?: Error | null;
  isLoading?: boolean;
  stats?: {
    followers: number;
    profileViews: number;
    subscriptionCount: number;
  };
};

export const ProfileStats = ({
  className,
  error,
  isLoading,
  stats,
}: ProfileStatsProps) => {
  if (isLoading) {
    return <section className={className}>Loading profile stats...</section>;
  }

  if (error) {
    return <section className={className}>Stats unavailable</section>;
  }

  if (!stats) {
    return <section className={className}>No stats yet</section>;
  }

  return (
    <section className={className}>
      <dl>
        <div>
          <dt>Followers</dt>
          <dd>{stats.followers}</dd>
        </div>
        <div>
          <dt>Views</dt>
          <dd>{stats.profileViews}</dd>
        </div>
        <div>
          <dt>Subscriptions</dt>
          <dd>{stats.subscriptionCount}</dd>
        </div>
      </dl>
    </section>
  );
};
```

