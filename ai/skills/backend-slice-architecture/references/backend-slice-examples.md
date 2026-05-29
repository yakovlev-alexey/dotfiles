# Backend Slice Examples

Use these examples when implementing `backend-slice-architecture`.

## Turborepo Shape

```text
apps/
  web/
  api/
    prisma/
      schema.prisma
    src/
      common/
        fastify-app.ts
        prisma.ts
        prisma-executor.ts
      slices/
        users/
          commands/
            create-user-command.ts
          domain/
            assert-user-can-be-created.ts
            normalize-user-email.ts
          endpoints/
            create-user-endpoint.ts
          plugins/
            users-plugin.ts
          queries/
            find-user-by-email-query.ts
          usecases/
            create-user-usecase.ts
packages/
  types/
    src/
      slices/
        users/
          user-contracts.ts
```

## Prisma Executor

Commands and queries accept an optional executor so transactional usecases can pass `tx`.

```ts
import type { Prisma, PrismaClient } from "@prisma/client";

export type PrismaExecutor = PrismaClient | Prisma.TransactionClient;
```

## Query

```ts
import type { User } from "@prisma/client";

import { prisma } from "../../../common/prisma";
import type { PrismaExecutor } from "../../../common/prisma-executor";

type FindUserByEmailInput = {
  email: string;
};

export const findUserByEmailQuery = async (
  input: FindUserByEmailInput,
  db: PrismaExecutor = prisma,
): Promise<User | null> => {
  return db.user.findUnique({
    where: {
      email: input.email,
    },
  });
};
```

## Command

```ts
import type { User } from "@prisma/client";

import { prisma } from "../../../common/prisma";
import type { PrismaExecutor } from "../../../common/prisma-executor";

type CreateUserInput = {
  email: string;
  name?: string | null;
};

export const createUserCommand = async (
  input: CreateUserInput,
  db: PrismaExecutor = prisma,
): Promise<User> => {
  return db.user.create({
    data: {
      email: input.email,
      name: input.name ?? null,
    },
  });
};
```

## Usecase

```ts
import type { User } from "@prisma/client";

import { createUserCommand } from "../commands/create-user-command";
import { assertUserCanBeCreated } from "../domain/assert-user-can-be-created";
import { normalizeUserEmail } from "../domain/normalize-user-email";
import { findUserByEmailQuery } from "../queries/find-user-by-email-query";

type CreateUserInput = {
  email: string;
  name?: string;
};

export const createUserUsecase = async (
  input: CreateUserInput,
): Promise<User> => {
  const email = normalizeUserEmail(input.email);
  const existingUser = await findUserByEmailQuery({ email });

  assertUserCanBeCreated(existingUser);

  return createUserCommand({
    email,
    name: input.name,
  });
};
```

## Transactional Usecase

```ts
import type { Project } from "@prisma/client";

import { prisma } from "../../../common/prisma";
import { findUserByIdQuery } from "../../users/queries/find-user-by-id-query";
import { addProjectOwnerMemberCommand } from "../commands/add-project-owner-member-command";
import { createProjectCommand } from "../commands/create-project-command";
import { assertUserCanCreateProject } from "../domain/assert-user-can-create-project";
import { normalizeProjectName } from "../domain/normalize-project-name";

type CreateProjectInput = {
  actorUserId: string;
  name: string;
};

export const createProjectUsecase = async (
  input: CreateProjectInput,
): Promise<Project> => {
  return prisma.$transaction(async (tx) => {
    const actor = await findUserByIdQuery({ id: input.actorUserId }, tx);
    assertUserCanCreateProject(actor);

    const project = await createProjectCommand(
      {
        name: normalizeProjectName(input.name),
        ownerId: input.actorUserId,
      },
      tx,
    );

    await addProjectOwnerMemberCommand(
      {
        projectId: project.id,
        userId: input.actorUserId,
      },
      tx,
    );

    return project;
  });
};
```

## Endpoint

```ts
import type { FastifyPluginAsyncZod } from "fastify-type-provider-zod";
import {
  CreateUserBodySchema,
  UserResponseSchema,
} from "@repo/types/slices/users/user-contracts";

import { createUserUsecase } from "../usecases/create-user-usecase";

export const createUserEndpoint: FastifyPluginAsyncZod = async (app) => {
  app.post(
    "/users",
    {
      schema: {
        body: CreateUserBodySchema,
        response: {
          201: UserResponseSchema,
        },
        summary: "Create user",
        tags: ["Users"],
      },
    },
    async (request, reply) => {
      const user = await createUserUsecase(request.body);

      return reply.code(201).send(
        UserResponseSchema.parse({
          createdAt: user.createdAt.toISOString(),
          email: user.email,
          id: user.id,
          name: user.name,
          updatedAt: user.updatedAt.toISOString(),
        }),
      );
    },
  );
};
```

