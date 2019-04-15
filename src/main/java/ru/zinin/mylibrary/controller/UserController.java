package ru.zinin.mylibrary.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import ru.zinin.mylibrary.domain.Role;
import ru.zinin.mylibrary.domain.User;
import ru.zinin.mylibrary.repos.UserRepo;
import ru.zinin.mylibrary.service.UserService;

import java.util.Arrays;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

@Controller
@RequestMapping("/user")
public class UserController {

    @Autowired
    UserRepo userRepo;

    @Autowired
    private UserService userService;

    @GetMapping
    @PreAuthorize("hasAuthority('ADMIN')")
    public String userList(Model model) {
        model.addAttribute("users", userRepo.findAll());
        return "user_list";
    }

    @GetMapping("{user}")
    @PreAuthorize("hasAuthority('ADMIN')")
    public String userEdit(
            @PathVariable User user,
            Model model
            ) {
        model.addAttribute("user", user);
        model.addAttribute("roles", Role.values());
        return "user_edit";
    }

    @PostMapping
    @PreAuthorize("hasAuthority('ADMIN')")
    public String saveUser(
            @RequestParam String username,
            @RequestParam("userId")User user,
            @RequestParam Map<String,String> form
            ) {
        user.setUsername(username);

        user.getRoles().clear();

        Set<String> roles = Arrays.stream(Role.values()).map(Role::name).collect(Collectors.toSet());

        for (String key : form.keySet()) {
            if (roles.contains(key)) {
                user.getRoles().add(Role.valueOf(key));
            }
        }

        userRepo.save(user);
        return "redirect:/user";
    }

    @GetMapping("/profile")
    public String getProfile(
            Model model,
            @AuthenticationPrincipal User user
    ) {
        model.addAttribute("username", user.getUsername());
        return "profile";
    }

    @PostMapping("/profile")
    public String updateProfile(
            @RequestParam String password,
            @AuthenticationPrincipal User user,
            Model model
    ) {
        if (password.length() < 5) {
            model.addAttribute("passwordError", "password less than 5 characters");
            model.addAttribute("username", user.getUsername());
            return "profile";
        }
        userService.updateProfile(password, user);
        return "redirect:/user/profile";
    }
}





















