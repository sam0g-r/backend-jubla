/*
  Warnings:

  - Added the required column `pastorContact` to the `Reservations` table without a default value. This is not possible if the table is not empty.
  - Added the required column `documentId` to the `User` table without a default value. This is not possible if the table is not empty.
  - Added the required column `gender` to the `User` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Reservations" ADD COLUMN     "pastorContact" TEXT NOT NULL;

-- AlterTable
ALTER TABLE "User" ADD COLUMN     "documentId" TEXT NOT NULL,
ADD COLUMN     "gender" TEXT NOT NULL,
ADD COLUMN     "instagramProfile" TEXT,
ADD COLUMN     "profession" TEXT;
