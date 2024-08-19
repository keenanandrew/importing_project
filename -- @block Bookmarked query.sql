-- @block Bookmarked query
-- @group Requests
-- @name Users for digest

SELECT name, email
from users
where status = 'active' and created_at > '2023-10-25'
and lower(substr(email, position('@' in email) + 1)) not in ('elsevier.com', 'springernature.com', 'us.nature.com', 'cn.springernature.com', 'nature.com', 'cn.nature.com')