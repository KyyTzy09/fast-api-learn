from datetime import datetime
from typing import List
from app.models.quest_folder_model import FolderStatus, QuestFolderRequestModel
from collections import Counter
from app.models.reflection_model import ReflectionType


class ReflectionAnalyticConverter:
    def folderStatCounter(self, data: List[QuestFolderRequestModel]):
        folderStats = {}

        for q in data:
            folderName = getattr(q, "folder", "Unknown")

            if folderName not in folderStats:
                folderStats[folderName] = {"completed": 0, "failed": 0}

            if q.isSuccess:
                folderStats[folderName]["completed"] += 1
            else:
                folderStats[folderName]["failed"] += 1

        return [
            {
                "folder": name,
                "completed": stat["completed"],
                "failed": stat["failed"],
            }
            for name, stat in folderStats.items()
        ]

    # Rate Keberhasilan / kegagalan
    def calculateRate(self, part, total):
        if total == 0:
            return 0
        return round((part / total) * 100, 2)

    # Counter Alasan terbanyak
    def reasonCounter(self, counter, data, status):
        for q in data:
            for r in getattr(q, "reflections", []):
                if r.type == status:
                    reason = (r.reason or "").strip().lower()
                    if reason:
                        counter[reason] += 1

        return [{"keyword": k, "count": v} for k, v in counter.most_common(3)]

    # Converter Utama
    def convert(self, data: List[QuestFolderRequestModel]):
        total = len(data)
        completed = sum(1 for q in data if q.isSuccess)
        failed = total - completed
        folderStats = self.folderStatCounter(data)
        dominantFailedFolder = None
        dominantSuccessFolder = None

        if folderStats:
            dominantFailedFolder = max(folderStats, key=lambda x: x["failed"])["folder"]
            dominantSuccessFolder = max(folderStats, key=lambda x: x["completed"])[
                "folder"
            ]

        hourCounter = Counter()
        for q in data:
            if q.isSuccess and q.completedAt:
                hour = datetime.fromisoformat(str(q.completedAt)).hour
                hourCounter[hour] += 1

        mostProductiveHour = None
        if hourCounter:
            mostProductiveHour = hourCounter.most_common(1)[0][0]

        # Failed Rate
        largeTotal = 0
        largeSuccess = 0
        largeFailed = 0

        for q in data:
            if getattr(q, "estimatedMin", 0) > 90:
                largeTotal += 1
                if q.isSuccess:
                    largeSuccess += 1
                else:
                    largeFailed += 1

        largeSuccessRate = self.calculateRate(largeSuccess, largeTotal)
        largeFailureRate = self.calculateRate(largeFailed, largeTotal)

        successCounter = Counter()
        topSuccessReasons = self.reasonCounter(
            successCounter, data, ReflectionType.SUCCESS
        )

        failureCounter = Counter()
        topFailureReasons = self.reasonCounter(
            failureCounter, data, ReflectionType.FAILED
        )

        weeklyAnalysist = {
            "totalQuest": total,
            "completed": completed,
            "failed": failed,
            "mostProductiveHour": mostProductiveHour,
            "largeQuestSuccessRate": largeSuccessRate,
            "largeQuestFailureRate": largeFailureRate,
            "topSuccessKeywords": topSuccessReasons,
            "topFailureKeywords": topFailureReasons,
            "dominantSuccessFolder": dominantSuccessFolder,
            "dominantFailedFolder": dominantFailedFolder,
            "folderStats": folderStats,
        }

        return weeklyAnalysist
