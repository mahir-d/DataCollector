class TableColumnName:

    Challenges = dict({
        "col_name_create": "challengeId VARCHAR(50) PRIMARY KEY, legacyId INT(255),directProjectId INT(255),status VARCHAR(10), trackType VARCHAR(20), type VARCHAR(20), name VARCHAR(512), description MEDIUMTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL, totalPrizeCost INT(255), winners VARCHAR(512),registrationStartDate DATETIME, registrationEndDate DATETIME, submissionStartDate DATETIME, submissionEndDate DATETIME, startDate DATETIME, endDate DATETIME, technologies VARCHAR(512), numOfSubmissions INT(4), numOfRegistrants INT(4), forumId INT(255)",
        "col_name_insert": "challengeId, legacyId,directProjectId ,status, trackType, type , name , description , totalPrizeCost, winners,registrationStartDate , registrationEndDate, submissionStartDate , submissionEndDate , startDate , endDate, technologies, numOfSubmissions, numOfRegistrants, forumId"
    })
    Challenge_Member_Mapping = dict({
        "col_name_create": "challengeId VARCHAR(50), memberHandle VARCHAR(50), submission Bool, winningPosition INT(255)",
        "col_name_insert": "challengeId, memberHandle, submission, winningPosition"
    })
    Members = dict({
        "col_name_create": "userId INT(255), memberHandle VARCHAR(512) PRIMARY KEY, DEVELOP Bool, DESIGN Bool, DATA_SCIENCE Bool, maxRating INT(255), track VARCHAR(512), subTrack VARCHAR(512), registrations INT(255), wins INT(255), user_entered MEDIUMTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL, participation_skill MEDIUMTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL",
        "col_name_insert": "userId, memberHandle , DEVELOP , DESIGN, DATA_SCIENCE, maxRating, track , subTrack , registrations , wins, user_entered, participation_skill"
    })
