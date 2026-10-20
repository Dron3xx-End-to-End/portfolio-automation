const pl = document.getElementById("pl");
const eng = document.getElementById("eng");

const translations = {
	// START PL TRANSLATIONS
	pl: {
		Welcome: "Witaj w moim portfolio",
		ViewGitHub: "Zobacz mój GitHub",

		AboutDescription1:
			"Jestem początkującym Cloud & DevOps Engineerem z pasją do AWS, automatyzacji, IaC oraz ciągłej integracji.",
		AboutDescription2:
			"Obecnie uczę się Azure oraz Google Cloud Platform, aby poszerzyć swoją wiedzę i umiejętności związane z chmurą.",
		AboutDescription3:
			"Moim celem jest automatyzacja i optymalizacja infrastruktury chmurowej oraz procesów.",

		TechnicalSkills: "Umiejętności techniczne",
		Cloud: "Chmura",
		Learning: "(w trakcie nauki)",
		Programming: "Programowanie",

		EducationCertifications: "Edukacja i certyfikaty",
		ViewCredly: "Zobacz na Credly",

		Projects: "Projekty",
		TechnologiesUsed: "Wykorzystane technologie:",

		AWSPortfolioWebsite: "Strona portfolio AWS",
		AWSPortfolioDescription: "Statyczna strona portfolio AWS wdrożona na S3.",

		WindowsVoiceAssistant: "Asystent głosowy dla systemu Windows",

		TerraformProject: "Projekt Terraform",
		TerraformProjectDescription:
			"Infrastruktura AWS utworzona przy użyciu Terraform.",

		AnsibleProject: "Projekt Ansible",

		AnsibleProjectDescription:
			"Konfiguracja i automatyzacja instancji AWS EC2 przy użyciu Ansible.",

		// AUTO-GENERATED PL TRANSLATIONS

		PortfolioAutomation: "Automatyzacja Portfolio",
		PortfolioAutomationDescription: "Automatyzacja GitHub Actions do przetwarzania aktualizacji projektów i synchronizacji ich z portfolio Cloud & DevOps.",


		StatusFinished: "Status: Zakończony",
		StatusInProgress: "Status: W trakcie",
		StatusCompleted: "Status: Ukończony",

		ContactMe: "Skontaktuj się ze mną",
		Copyright: "© 2026 Dawid Bronikowski. Wszelkie prawa zastrzeżone.",
		LastUpdated: "Ostatnia aktualizacja:",
	},
	// END PL TRANSLATIONS
	// START ENG TRANSLATIONS
	eng: {
		Welcome: "Welcome to My Portfolio",
		ViewGitHub: "View my GitHub",

		AboutDescription1:
			"I'm an aspiring Cloud & DevOps Engineer with a passion for AWS, automation, IaC and continuous integration.",
		AboutDescription2:
			"I am currently learning Azure and Google Cloud Platform to expand my cloud expertise.",
		AboutDescription3:
			"My goal is to automate and optimize cloud infrastructure and workflows.",

		TechnicalSkills: "Technical Skills",
		Cloud: "Cloud",
		Learning: "(learning)",
		Programming: "Programming",

		EducationCertifications: "Education & Certifications",
		ViewCredly: "View on Credly",

		Projects: "Projects",
		TechnologiesUsed: "Technologies used:",

		AWSPortfolioWebsite: "AWS Portfolio Website",
		AWSPortfolioDescription: "Static AWS portfolio website deployed on S3.",

		WindowsVoiceAssistant: "Windows Voice Assistant",

		TerraformProject: "Terraform Project",
		TerraformProjectDescription: "AWS infrastructure with Terraform.",

		AnsibleProject: "Ansible Project",

		AnsibleProjectDescription:
			"Configuration and automation of AWS EC2 instances using Ansible.",

		// AUTO-GENERATED ENG TRANSLATIONS

		PortfolioAutomation: "Portfolio Automation",
		PortfolioAutomationDescription: "GitHub Actions automation for automatically processing project updates and synchronizing them with a Cloud & DevOps portfolio.",


		StatusInProgress: "Status: In progress",
		StatusCompleted: "Status: Completed",

		ContactMe: "Contact me",
		Copyright: "© 2026 Dawid Bronikowski. All rights reserved.",
		LastUpdated: "Last updated:",
	},
	// END ENG TRANSLATIONS
};

function changeLanguage(language) {
	const selectedLanguage = translations[language];
	selectedLanguage &&
		Object.keys(selectedLanguage).forEach((key) => {
			const elements = document.querySelectorAll(`[data-i18n="${key}"]`);
			elements.forEach((el) => {
				el.textContent = selectedLanguage[key];
			});
		});
	console.log("Language changed to:", language);
}

pl.addEventListener("click", () => changeLanguage("pl"));
eng.addEventListener("click", () => changeLanguage("eng"));
