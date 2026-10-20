const left = document.getElementById("arrow-left");
const right = document.getElementById("arrow-right");
const projectMove = document.getElementById("project-move");
const projects = projectMove
	? Array.from(projectMove.children).find((el) => el.tagName === "UL")
	: null;

if (!projectMove || !projects || !left || !right) {
	console.warn("Project carousel elements not found.");
} else {
	let currentIndex = 0;

	const getStepSize = () => {
		const firstProject = projects.querySelector(".project-item");
		if (!firstProject) {
			return 0;
		}

		const styles = window.getComputedStyle(firstProject);
		const marginLeft = parseFloat(styles.marginLeft || "0");
		const marginRight = parseFloat(styles.marginRight || "0");
		const width =
			firstProject.getBoundingClientRect().width || firstProject.offsetWidth;
		return Math.ceil(width + marginLeft + marginRight);
	};

	const updateArrows = () => {
		const items = projects.querySelectorAll(".project-item");
		const maxScrollLeft = Math.max(
			0,
			projects.scrollWidth - projects.clientWidth,
		);
		projects.classList.toggle("is-centered", maxScrollLeft === 0);
		if (!items.length || items.length === 1 || maxScrollLeft === 0) {
			left.style.visibility = "hidden";
			left.style.pointerEvents = "none";
			right.style.visibility = "hidden";
			right.style.pointerEvents = "none";
			return;
		}

		left.style.visibility = projects.scrollLeft > 1 ? "visible" : "hidden";
		left.style.pointerEvents = projects.scrollLeft > 1 ? "auto" : "none";
		right.style.visibility =
			projects.scrollLeft < maxScrollLeft - 1 ? "visible" : "hidden";
		right.style.pointerEvents =
			projects.scrollLeft < maxScrollLeft - 1 ? "auto" : "none";
	};

	const renderPosition = () => {
		const step = getStepSize();
		if (!step) {
			return;
		}

		const maxIndex = Math.max(
			0,
			projects.querySelectorAll(".project-item").length - 1,
		);
		currentIndex = Math.min(Math.max(currentIndex, 0), maxIndex);
		projects.scrollLeft = currentIndex * step;
		updateArrows();
	};

	const moveProjects = (direction) => {
		const items = Array.from(projects.querySelectorAll(".project-item"));
		if (!items.length) {
			return;
		}

		const maxIndex = items.length - 1;
		currentIndex = Math.min(Math.max(currentIndex + direction, 0), maxIndex);
		renderPosition();
	};

	left.addEventListener("click", () => moveProjects(-1));
	right.addEventListener("click", () => moveProjects(1));
	projects.addEventListener("scroll", updateArrows);
	window.addEventListener("resize", renderPosition);

	renderPosition();
}
