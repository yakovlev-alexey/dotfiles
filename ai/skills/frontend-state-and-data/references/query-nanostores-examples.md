# Query And Nano Stores Examples

Use these examples when implementing `frontend-state-and-data`.

## Nano Store Model

```ts
import { map } from "nanostores";

export type ProfileFilters = {
  period: "week" | "month";
};

export const $profileFilters = map<ProfileFilters>({
  period: "month",
});
```

## Frontend State Command

```ts
import type { ProfileFilters } from "../model/profile-filters-store";
import { $profileFilters } from "../model/profile-filters-store";

export const setProfilePeriodCommand = (period: ProfileFilters["period"]) => {
  $profileFilters.setKey("period", period);
};
```

## Query Options

```ts
import { queryOptions } from "@tanstack/react-query";

import type { ProfileFilters } from "../model/profile-filters-store";

export const profileStatsQuery = (filters: ProfileFilters) =>
  queryOptions({
    queryKey: ["profile-stats", filters],
    queryFn: async () => {
      const response = await fetch(`/api/profile/stats?period=${filters.period}`);

      if (!response.ok) {
        throw new Error("Failed to load profile stats");
      }

      return response.json();
    },
  });
```

## Server Mutation With Command

```ts
import type { ProfileDraft } from "../model/profile-draft-store";

export const saveProfileCommand = async (draft: ProfileDraft) => {
  const response = await fetch("/api/profile", {
    body: JSON.stringify(draft),
    headers: {
      "Content-Type": "application/json",
    },
    method: "PUT",
  });

  if (!response.ok) {
    throw new Error("Failed to save profile");
  }

  return response.json();
};
```

```tsx
import { useStore } from "@nanostores/react";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { saveProfileCommand } from "../../store/commands/save-profile-command";
import { $profileDraft } from "../../store/model/profile-draft-store";

export const SaveProfileWidget = () => {
  const draft = useStore($profileDraft);
  const queryClient = useQueryClient();

  const saveProfileMutation = useMutation({
    mutationFn: saveProfileCommand,
    onSuccess: async (profile) => {
      queryClient.setQueryData(["profile", profile.id], profile);
      await queryClient.invalidateQueries({ queryKey: ["profile"] });
    },
  });

  return (
    <button
      disabled={saveProfileMutation.isPending}
      onClick={() => saveProfileMutation.mutate(draft)}
      type="button"
    >
      Save
    </button>
  );
};
```

