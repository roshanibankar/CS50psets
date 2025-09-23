document.addEventListener('DOMContentLoaded', () => {

    // CSRF helper for Django POST/PUT/DELETE requests
    function getCSRFToken() {
        const name = 'csrftoken';
        const cookies = document.cookie.split(';');
        for (let c of cookies) {
            c = c.trim();
            if (c.startsWith(name + '=')) {
                return decodeURIComponent(c.slice(name.length + 1));
            }
        }
        return '';
    }
    const csrftoken = getCSRFToken();

    // Like / Unlike Posts
    document.querySelectorAll('.like-btn').forEach(button => {
        button.onclick = () => {
            const postId = button.dataset.id;
            fetch(`/like/${postId}`, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }
                button.innerText = data.liked ? "Unlike" : "Like";
                const likeCountSpan = button.parentElement.querySelector('.like-count');
                likeCountSpan.innerText = data.likes;
            });
        };
    });

    // Edit Posts Inline (single implementation)
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.onclick = () => {
            const postId = button.dataset.id;
            const postDiv = document.querySelector(`#post-${postId}`);
            const contentP = postDiv.querySelector('.post-content') || postDiv.querySelector('p');
            const originalContent = contentP.innerText;

            // Create textarea and save button
            const textarea = document.createElement("textarea");
            textarea.className = "form-control";
            textarea.value = originalContent;

            const saveBtn = document.createElement("button");
            saveBtn.className = "btn btn-sm btn-success mt-2";
            saveBtn.innerText = "Save";

            // Replace content with editor
            contentP.replaceWith(textarea);
            button.style.display = "none";  // Hide Edit
            postDiv.appendChild(saveBtn);

            saveBtn.onclick = () => {
                const updatedContent = textarea.value.trim();
                if (!updatedContent) {
                    alert("Content cannot be empty.");
                    return;
                }
                fetch(`/edit/${postId}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrftoken
                    },
                    body: JSON.stringify({ content: updatedContent })
                })
                .then(response => {
                    if (!response.ok) throw new Error("Failed to update post");
                    return response.json();
                })
                .then(() => {
                    // Replace textarea with updated content
                    const updatedP = document.createElement("p");
                    updatedP.className = "post-content";
                    updatedP.innerText = updatedContent;
                    textarea.replaceWith(updatedP);
                    saveBtn.remove();
                    button.style.display = "inline-block";
                })
                .catch(error => alert(error.message));
            };
        };
    });

    // Follow / Unfollow on Profile page
    const followButton = document.querySelector('#follow-button');
    if (followButton) {
        followButton.onclick = () => {
            const username = followButton.dataset.username;

            fetch(`/follow/${username}`, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }
                followButton.innerText = data.message === "Followed" ? "Unfollow" : "Follow";

                // Optionally update follower count dynamically:
                const followersCountSpan = document.querySelector('#followers-count');
                if (followersCountSpan && data.followers_count !== undefined) {
                    followersCountSpan.innerText = data.followers_count;
                }
            });
        };
    }

});
